package com.an2t.myapplication.home.ui.dashboard

import android.annotation.SuppressLint
import android.content.Context
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.LinearLayout
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentActivity
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.viewpager2.adapter.FragmentStateAdapter
import androidx.viewpager2.widget.ViewPager2
import com.an2t.myapplication.R
import com.an2t.myapplication.databinding.FragmentDashboardBinding
import com.an2t.myapplication.home.ui.home.adapters.DashMatchAdapter
import com.an2t.myapplication.model.*
import com.an2t.myapplication.utils.AppConstants
import com.an2t.myapplication.view_pager_test.DogMatchResultsMapsFragment
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
import java.lang.IllegalStateException
import java.util.*
import kotlin.concurrent.schedule


//import com.an2t.myapplication.home1.databinding.FragmentDashboardBinding

class DashboardFragment : Fragment(), OnMapReadyCallback, GoogleMap.OnCameraMoveListener,
    GoogleMap.OnCameraIdleListener, GoogleMap.OnInfoWindowClickListener,
    GoogleMap.OnPolylineClickListener,
    DogMatchResultsMapsFragment.OnMatchedResListener {

    private var mMap: GoogleMap? = null
    var zoomLevel = 12.5f


    private var _binding: FragmentDashboardBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    private lateinit var dashboardViewModel: DashboardViewModel
    private lateinit var matchResultsAdapter: DashMatchAdapter
    private var mGeoApiContext: GeoApiContext? = null
    private var mPolyLinesData: ArrayList<PolylineData> = ArrayList()

    private var mainResList: ArrayList<Match>? = ArrayList()

    private lateinit var dogMatchFragment: DogMatchResultsMapsFragment

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        dashboardViewModel =
            ViewModelProvider(this).get(DashboardViewModel::class.java)

        _binding = FragmentDashboardBinding.inflate(inflater, container, false)
        val root: View = binding.root
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

//       The pager adapter, which provides the pages to the view pager widget.
//       val pagerAdapter = ScreenSlidePagerAdapter(requireActivity())
//       _binding?.vpShowMatchResults?.adapter = pagerAdapter
    }


    private fun setUpMaps() {
        val mapFragment =
            childFragmentManager.findFragmentById(com.an2t.myapplication.R.id.map) as SupportMapFragment
        mapFragment.getMapAsync(this)

        if (mGeoApiContext == null) {
            mGeoApiContext = GeoApiContext.Builder()
                .apiKey(context?.getString(com.an2t.myapplication.R.string.google_maps_api_key))
                .build()
        }
    }

    private fun calculateDirections(marker: ClusterMarker) {
        print("calculateDirections: calculating directions.")
        val destination = com.google.maps.model.LatLng(
            marker.position.latitude,
            marker.position.longitude
        )
        val directions = DirectionsApiRequest(mGeoApiContext)
        directions.alternatives(true)
        directions.origin(
            com.google.maps.model.LatLng(
                selectedMatch.lat!!.toDouble(),
                selectedMatch.lng!!.toDouble()
            )
        )
        print("calculateDirections: destination: $destination")
        directions.destination(destination)
            .setCallback(object : PendingResult.Callback<DirectionsResult?> {
                override fun onFailure(e: Throwable?) {

                }

                override fun onResult(result: DirectionsResult?) {
//                    print("onResult: routes: " + result!!.routes[0].toString())
//                    print("onResult: durations: " + result!!.routes[0].legs[0].duration.toString())
//                    print("onResult: distance: " + result!!.routes[0].legs[0].distance.toString())
//                    print("onResult: geocodedWayPoints: " + result.geocodedWaypoints[0].toString())
                    result?.let { r->
                        val distance = r.routes[0].legs[0].distance.toString()
                        val duration = r.routes[0].legs[0].duration.toString()
                        addPolylinesToMap(r)
                        Handler(Looper.getMainLooper()).post(Runnable {
                            dogMatchFragment.updateDurationAndDistance(distance, duration)
                            result.routes[0].legs[0]

                        })
                    }


                }


            })
    }

    private fun addPolylinesToMap(result: DirectionsResult) {
        Handler(Looper.getMainLooper()).post(Runnable {
            try{
                val _ac = requireActivity()
                if(_ac != null){
                    if (mPolyLinesData.size > 0) {
                        for (polylineData in mPolyLinesData) {
                            polylineData.polyline.remove()
                        }
                        mPolyLinesData.clear()
                        mPolyLinesData = ArrayList()
                    }
                    for (route in result.routes) {
//                print("run: leg: " + route.legs[0].toString())
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
                        polyline.color =
                            ContextCompat.getColor(_ac, com.an2t.myapplication.R.color.gray)
                        polyline.isClickable = true
                        mPolyLinesData.add(PolylineData(polyline, route.legs[0]))
                        activateFirstPolyline()
                    }
                }
            }catch (e: IllegalStateException){
                print(e.message.toString())
            }
        })
    }


    private fun hideProgress() {
//        binding.pbShow.visibility = View.GONE
        binding.llProgress.visibility = View.GONE
        _binding?.clMainMapView?.visibility = View.VISIBLE
    }

    private fun showProgress() {
//        binding.pbShow.visibility = View.VISIBLE
        binding.llProgress.visibility = View.VISIBLE
        binding.animationView.setAnimation(R.raw.purple_dog_walking)
        binding.animationView.playAnimation()
        binding.animationView.loop(true)
        _binding?.clMainMapView?.visibility = View.GONE
    }

    private lateinit var selectedMatch: Match

    private fun _observe() {


        dashboardViewModel.l_res.observe(viewLifecycleOwner) { l_res ->
            l_res?.status?.let {
                hideProgress()
                if (it) {


                    if(l_res.matchList.isNullOrEmpty()){
                        showNoDataFound()
                    }

                    if (0 < l_res.matchList?.size!!) {
                        selectedMatch = l_res.matchList[0]
                        plotMultipleMarkers(selectedMatch, selectedMatch.finalOutput)
                    }
                    l_res.matchList?.let {
                        mainResList?.clear()
                        mainResList?.addAll(it)
                        val pagerAdapter = ScreenSlidePagerAdapter(requireActivity())

                        _binding?.vpShowMatchResults?.adapter = pagerAdapter

                        _binding?.vpShowMatchResults?.registerOnPageChangeCallback(object :
                            ViewPager2.OnPageChangeCallback() {
                            override fun onPageSelected(position: Int) {
                                selectedMatch = l_res.matchList[position]
                                plotMultipleMarkers(selectedMatch, selectedMatch.finalOutput)
                                calculateDirections(mClusterMarkers[0])
                                dogMatchFragment = pagerAdapter.fragments[position]
                                shouldZoomInPolyPath = true
                                super.onPageSelected(position)
                            }
                        })
//                        matchResultsAdapter.apply {
//                            setListData(it)
//                            notifyDataSetChanged()
//                        }
                    }
                }
            }
        }
    }


    private fun showNoDataFound() {
        binding.llProgress.visibility = View.VISIBLE
        binding.animationView.setAnimation(R.raw.error_state_dog)
        binding.animationView.playAnimation()
        binding.animationView.loop(true)
        binding.tvProgressTitle.text = resources.getString(R.string.no_records_found)
        binding.tvProgressTitle.textSize = 16.0f
        _binding?.clMainMapView?.visibility = View.GONE
        val params: LinearLayout.LayoutParams =
            LinearLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT)
        params.setMargins(0, -50, 0, 0)
        binding.tvProgressTitle.layoutParams = params
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

    private fun plotMultipleMarkers(selectedMatch: Match, finalOutput: ArrayList<FinalOutput>?) {
        finalOutput?.let { fo ->
            addMapMaker(selectedMatch, fo)
        }

    }

    private fun plotMarker(
        userLatitude: String,
        userLongitude: String
    ) {
        val defaultLocationOnMap = LatLng(userLatitude.toDouble(), userLongitude.toDouble())
        mMap?.addMarker(MarkerOptions().position(defaultLocationOnMap).title("Marker"))
        val cameraPosition =
            CameraPosition.Builder().target(defaultLocationOnMap).zoom(zoomLevel).build()
        mMap?.moveCamera(CameraUpdateFactory.newCameraPosition(cameraPosition))
    }


    private var mClusterManager: ClusterManager<ClusterMarker>? = null
    private lateinit var mClusterManagerRenderer: CustomClusterManagerRender
    private val mClusterMarkers: ArrayList<ClusterMarker> = ArrayList()

    @SuppressLint("PotentialBehaviorOverride")
    private fun addMapMaker(selectedMatch: Match, fo: ArrayList<FinalOutput>) {
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

            mClusterManager?.clearItems()
            mClusterMarkers.clear()

            try {
                var snippet = ""
                val avatar: Int = com.an2t.myapplication.R.drawable.ic_map_pin

                val ffo = FinalOutput(
                    selectedMatch.lat!!.toDouble(),
                    selectedMatch.lng!!.toDouble(),
                    1.0,
                    -1,
                    selectedMatch.imageUrl,
                    selectedMatch.userId,
                    selectedMatch.contact_email
                )
                val newClusterMarker = ClusterMarker(
                    LatLng(
                        selectedMatch.lat.toDouble(),
                        selectedMatch.lng.toDouble()
                    ),
                    "",
                    snippet,
                    avatar,
                    ffo
                )
                mClusterManager?.addItem(newClusterMarker)
                mClusterMarkers.add(newClusterMarker)
            } catch (e: NullPointerException) {
                print("addMapMarkers: NullPointerException: " + e.message)
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
                        "",
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
            setCameraView(selectedMatch)
//            mClusterManager?.markerCollection?.setOnInfoWindowClickListener{ marker ->
//                calculateDirections(marker)
//                print("Hello")
//            }
        }
    }


    private var mMapBoundary: LatLngBounds? = null

    /**
     * Determines the view boundary then sets the camera
     * Sets the view
     */
    private fun setCameraView(m: Match) {
        val defaultLocationOnMap = LatLng(m.lat!!.toDouble(), m.lng!!.toDouble())
        val cameraPosition =
            CameraPosition.Builder().target(defaultLocationOnMap).zoom(zoomLevel).build()
        mMap?.animateCamera(CameraUpdateFactory.newCameraPosition(cameraPosition))
    }

    override fun onInfoWindowClick(p0: Marker) {
        print("Hello")
    }

    override fun onPolylineClick(polyline: Polyline) {
        for (polylineData in mPolyLinesData) {
            print("onPolylineClick: toString: " + polylineData.toString())
            if (polyline.id.equals(polylineData.polyline.id)) {
                polylineData.polyline.color = ContextCompat.getColor(
                    requireActivity(),
                    com.an2t.myapplication.R.color.purple_200
                )
                polylineData.polyline.zIndex = 1F

                val dur = polylineData.leg.duration.toString()
                val dis = polylineData.leg.distance.toString()

                Handler(Looper.getMainLooper()).post(Runnable {
                    dogMatchFragment.updateDurationAndDistance(dis, dur)
                    zoomRoute(polyline.points)
                })


            } else {
                polylineData.polyline
                    .color =
                    ContextCompat.getColor(requireActivity(), com.an2t.myapplication.R.color.gray)
                polylineData.polyline.zIndex = 0F
            }
        }
    }

    var shouldZoomInPolyPath = true

    fun activateFirstPolyline(){
        mPolyLinesData[0].polyline.color = ContextCompat.getColor(
            requireActivity(),
            com.an2t.myapplication.R.color.purple_200
        )
        mPolyLinesData[0].polyline.zIndex = 1F
        if(!shouldZoomInPolyPath){
            zoomRoute(mPolyLinesData[0].polyline.points)
        }
        shouldZoomInPolyPath = false
    }

    private inner class ScreenSlidePagerAdapter(fa: FragmentActivity) : FragmentStateAdapter(fa) {
        val fragments: MutableList<DogMatchResultsMapsFragment> = mutableListOf()
        override fun getItemCount(): Int = mainResList?.size!!

        override fun createFragment(position: Int): Fragment  {
            val _f = DogMatchResultsMapsFragment.newInstance(mainResList?.get(position)!!, position)
            fragments.add(_f)
            return _f
        }

    }

    fun zoomRoute(lstLatLngRoute: List<LatLng?>?) {
        if (mMap == null || lstLatLngRoute == null || lstLatLngRoute.isEmpty()) return
        val boundsBuilder = LatLngBounds.Builder()
        for (latLngPoint in lstLatLngRoute) boundsBuilder.include(latLngPoint)
        val routePadding = 200
        val latLngBounds = boundsBuilder.build()
        mMap?.animateCamera(

            CameraUpdateFactory.newLatLngBounds(latLngBounds, routePadding),
            600,
            null
        )
    }

    override fun onMatchedResClick(finalOutput: FinalOutput, itemNumber: Int) {
        calculateDirections(mClusterMarkers[itemNumber + 1])
    }
}