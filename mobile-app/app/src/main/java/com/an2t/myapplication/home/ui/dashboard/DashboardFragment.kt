package com.an2t.myapplication.home.ui.dashboard

import android.annotation.SuppressLint
import android.content.Context
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import com.an2t.myapplication.databinding.FragmentDashboardBinding
import com.an2t.myapplication.home.ui.home.adapters.DashMatchAdapter
import com.an2t.myapplication.model.*
import com.an2t.myapplication.utils.AppConstants
import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.SupportMapFragment
import com.google.android.gms.maps.model.*
import com.google.maps.DirectionsApiRequest
import com.google.maps.GeoApiContext
import com.google.maps.PendingResult
import com.google.maps.android.clustering.ClusterManager
import com.google.maps.internal.PolylineEncoding
import com.google.maps.model.DirectionsResult


//import com.an2t.myapplication.home1.databinding.FragmentDashboardBinding

class DashboardFragment : Fragment(), OnMapReadyCallback, GoogleMap.OnCameraMoveListener,
    GoogleMap.OnCameraIdleListener,  GoogleMap.OnInfoWindowClickListener, GoogleMap.OnPolylineClickListener {

    private var mMap: GoogleMap? = null
    var zoomLevel = 12.5f


    private var _binding: FragmentDashboardBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    private lateinit var dashboardViewModel : DashboardViewModel
    private lateinit var matchResultsAdapter: DashMatchAdapter
    private var mGeoApiContext: GeoApiContext? = null
    private var mPolyLinesData: ArrayList<PolylineData> = ArrayList()

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        dashboardViewModel =
            ViewModelProvider(this).get(DashboardViewModel::class.java)

        _binding = FragmentDashboardBinding.inflate(inflater, container, false)
        val root: View = binding.root

//        val textView: TextView = binding.textDashboard
//        dashboardViewModel.text.observe(viewLifecycleOwner) {
//            textView.text = it
//        }
        return root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        setUpMaps()

        showProgress()
        _binding?.rvShowMatchResults!!.apply {
            layoutManager = LinearLayoutManager(activity, LinearLayoutManager.HORIZONTAL, false)
//            val decoration = DividerItemDecoration(activity, DividerItemDecoration.VERTICAL)
//            addItemDecoration(decoration)
            matchResultsAdapter = DashMatchAdapter()
            adapter = matchResultsAdapter
        }

        val refresh_token = getRefreshToken()
        val fcm_token = getFCMToken()
        dashboardViewModel.callMatchRecords(refresh_token, fcm_token)

        _observe()
    }

    private fun setUpMaps() {
        val mapFragment = childFragmentManager.findFragmentById(com.an2t.myapplication.R.id.map) as SupportMapFragment
        mapFragment.getMapAsync(this)

        if (mGeoApiContext == null) {
            mGeoApiContext = GeoApiContext.Builder()
                .apiKey(context?.getString(com.an2t.myapplication.R.string.google_maps_api_key))
                .build()
        }
    }

    private fun calculateDirections(marker: Marker) {
        print("calculateDirections: calculating directions.")
        val destination = com.google.maps.model.LatLng(
            marker.getPosition().latitude,
            marker.getPosition().longitude
        )
        val directions = DirectionsApiRequest(mGeoApiContext)
        directions.alternatives(true)
        directions.origin(
            com.google.maps.model.LatLng(
                selectedMatch.finalOutput?.get(0)?.lat!!.toDouble(),
                selectedMatch.finalOutput?.get(0)?.lng!!.toDouble()
            )
        )
        print("calculateDirections: destination: $destination")
        directions.destination(destination).setCallback(object : PendingResult.Callback<DirectionsResult?> {
            override fun onFailure(e: Throwable?) {

            }

            override fun onResult(result: DirectionsResult?) {
                print("onResult: routes: " + result!!.routes[0].toString())
                print("onResult: durations: " + result!!.routes[0].legs[0].duration.toString())
                print("onResult: distance: " + result!!.routes[0].legs[0].distance.toString())
                print("onResult: geocodedWayPoints: " + result.geocodedWaypoints[0].toString())
                addPolylinesToMap(result)
            }


        })
    }

    private fun addPolylinesToMap(result: DirectionsResult) {
        Handler(Looper.getMainLooper()).post(Runnable {
            print("run: result routes: " + result.routes.size)
            if (mPolyLinesData.size > 0) {
                for (polylineData in mPolyLinesData) {
                    polylineData.polyline.remove()
                }
                mPolyLinesData.clear()
                mPolyLinesData = ArrayList()
            }
            for (route in result.routes) {
                print("run: leg: " + route.legs[0].toString())
                val decodedPath = PolylineEncoding.decode(route.overviewPolyline.encodedPath)
                val newDecodedPath: MutableList<LatLng> = ArrayList()

                // This loops through all the LatLng coordinates of ONE polyline.
                for (latLng in decodedPath) {

//                        Log.d(TAG, "run: latlng: " + latLng.toString());
                    newDecodedPath.add(
                        LatLng(
                            latLng.lat,
                            latLng.lng
                        )
                    )
                }
                val polyline: Polyline =
                    mMap!!.addPolyline(PolylineOptions().addAll(newDecodedPath))
                polyline.color = ContextCompat.getColor(requireActivity(), com.an2t.myapplication.R.color.gray)
                polyline.isClickable = true
                mPolyLinesData.add(PolylineData(polyline, route.legs[0]))
            }
        })
    }


    private fun hideProgress() {
        binding.pbShow.visibility = View.GONE
        _binding?.rvShowMatchResults?.visibility = View.VISIBLE
    }

    private fun showProgress() {
        binding.pbShow.visibility = View.VISIBLE
        _binding?.rvShowMatchResults?.visibility = View.GONE
    }

    private lateinit var selectedMatch : Match

    private fun _observe() {
        dashboardViewModel.l_res.observe(viewLifecycleOwner) { l_res ->
            l_res?.status?.let {
                hideProgress()
                if (it) {

                    if (0 < l_res.matchList?.size!!) {
                        selectedMatch = l_res.matchList[0]
                        plotMultipleMarkers(selectedMatch.finalOutput)
                    }
                    l_res.matchList?.let {
                        matchResultsAdapter.apply {
                            setListData(it)
                            notifyDataSetChanged()
                        }
                    }
                }
            }
        }
    }


    private fun getFCMToken(): String {
        val sharedPreference =
            activity?.getSharedPreferences(AppConstants.SHARED_PREF_DOG_APP, Context.MODE_PRIVATE)
        val fcm_t = sharedPreference?.getString(AppConstants.FCM_TOKEN, "")
        return fcm_t!!
    }

    private fun getRefreshToken(): String {
        val sharedPreference =
            activity?.getSharedPreferences(AppConstants.SHARED_PREF_DOG_APP, Context.MODE_PRIVATE)
        val refresh_token = sharedPreference?.getString(AppConstants.REFRESH_TOKEN, "")
        return refresh_token!!
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

    override fun onMapReady(googleMap: GoogleMap) {
        mMap = googleMap
        mMap?.setOnCameraMoveListener(this)
        mMap?.setOnCameraIdleListener(this)
        mMap?.setOnPolylineClickListener(this)
    }

    internal class MarkerClick : GoogleMap.OnInfoWindowClickListener {
        override fun onInfoWindowClick(marker: Marker) {
            println(marker.title)
        }
    }

    override fun onCameraMove() {

    }

    override fun onCameraIdle() {

    }

    private fun plotMultipleMarkers(finalOutput: List<FinalOutput>?) {
        finalOutput?.let { fo->
            addMapMaker(fo)
        }

    }




    private fun plotMarker(
        userLatitude: String,
        userLongitude: String
    ) {


        val defaultLocationOnMap = LatLng(userLatitude.toDouble(), userLongitude.toDouble())

//        addMapMaker()
        mMap?.addMarker(MarkerOptions().position(defaultLocationOnMap).title("Marker"))
        val cameraPosition =
            CameraPosition.Builder().target(defaultLocationOnMap).zoom(zoomLevel).build()
        mMap?.moveCamera(CameraUpdateFactory.newCameraPosition(cameraPosition))
    }


    private var mClusterManager: ClusterManager<ClusterMarker>? = null
    private lateinit var mClusterManagerRenderer : CustomClusterManagerRender
    private val mClusterMarkers: ArrayList<ClusterMarker> = ArrayList()

    @SuppressLint("PotentialBehaviorOverride")
    private fun addMapMaker(fo: List<FinalOutput>) {
        if (mMap != null) {
            if (mClusterManager == null) {
                mClusterManager =
                    ClusterManager<ClusterMarker>(activity?.applicationContext, mMap)
            }
            if (!::mClusterManagerRenderer.isInitialized) {
                mClusterManagerRenderer = CustomClusterManagerRender(
                    activity,
                    mMap,
                    mClusterManager
                )
                mClusterManager!!.setRenderer(mClusterManagerRenderer)
            }

            for (userLocation in fo) {

                try {
                    var snippet = ""
                    val avatar: Int = com.an2t.myapplication.R.drawable.ic_map_pin
                    val newClusterMarker = ClusterMarker(
                        LatLng(
                            userLocation.lat!!.toDouble(),
                            userLocation.lng!!.toDouble()
                        ),
                        "Some Name",
                        snippet,
                        avatar,
                        userLocation
                    )
                    mClusterManager?.addItem(newClusterMarker)
                    mClusterMarkers.add(newClusterMarker)
                } catch (e: NullPointerException) {
                    print("addMapMarkers: NullPointerException: " + e.message)
                }
            }
            mClusterManager?.cluster()
            setCameraView(fo[0])

            mClusterManager?.markerCollection?.setOnInfoWindowClickListener{ marker ->
                calculateDirections(marker)
                print("Hello")
            }

//            mMap!!.setOnInfoWindowClickListener { marker ->
//                print("Hello")
//            }

            //Set this only once:

            //Set this only once:
//            mMap?.setOnInfoWindowClickListener(this)
        }
    }


    private var mMapBoundary: LatLngBounds? = null
    /**
     * Determines the view boundary then sets the camera
     * Sets the view
     */
    private fun setCameraView(finalOutput: FinalOutput) {

        // Set a boundary to start
//        val bottomBoundary: Double = finalOutput.lat!!.toDouble().minus(.1)
//        val leftBoundary: Double = finalOutput.lng!!.toDouble().minus(.1)
//        val topBoundary: Double = finalOutput.lat.toDouble() + .1
//        val rightBoundary: Double = finalOutput.lng.toDouble() + .1
//        mMapBoundary = LatLngBounds(
//            LatLng(bottomBoundary, leftBoundary),
//            LatLng(topBoundary, rightBoundary)
//        )
//        mMapBoundary?.let {
//            mMap?.moveCamera();
//        }
//        val cameraPosition =
//            CameraPosition.Builder().target(mMapBoundary).zoom(zoomLevel).build()
        val defaultLocationOnMap = LatLng(finalOutput.lat!!.toDouble(), finalOutput.lng!!.toDouble())
//        addMapMaker()
        mMap?.addMarker(MarkerOptions().position(defaultLocationOnMap).title("Marker"))
        val cameraPosition =
            CameraPosition.Builder().target(defaultLocationOnMap).zoom(zoomLevel).build()
        mMap?.moveCamera(CameraUpdateFactory.newCameraPosition(cameraPosition))
//        val cameraPosition =
//            CameraPosition.Builder().target(defaultLocationOnMap).zoom(zoomLevel).build()
//        mMap?.moveCamera(CameraUpdateFactory.newCameraPosition(cameraPosition))
//        mMap?.moveCamera(CameraUpdateFactory.newLatLngBounds(mMapBoundary, 0))
    }

    override fun onInfoWindowClick(p0: Marker) {
        print("Hello")
    }

    override fun onPolylineClick(polyline: Polyline) {
        for (polylineData in mPolyLinesData) {
            print("onPolylineClick: toString: " + polylineData.toString())
            if (polyline.getId().equals(polylineData.getPolyline().getId())) {
                polylineData.getPolyline()
                    .setColor(ContextCompat.getColor(requireActivity(), com.an2t.myapplication.R.color.purple_200))
                polylineData.getPolyline().setZIndex(1F)
//                print(polylineData.leg.distance)
            } else {
                polylineData.getPolyline()
                    .setColor(ContextCompat.getColor(requireActivity(), com.an2t.myapplication.R.color.gray))
                polylineData.getPolyline().setZIndex(0F)
            }
        }
    }
}