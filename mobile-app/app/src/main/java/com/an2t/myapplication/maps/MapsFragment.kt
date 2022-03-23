package com.an2t.myapplication.maps

import android.Manifest
import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.location.Address
import android.location.Geocoder
import android.location.Location
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AppCompatDialogFragment
import androidx.core.content.ContextCompat
import com.an2t.myapplication.R
import com.an2t.myapplication.databinding.FragmentMapsBinding
import com.an2t.myapplication.model.LoginRes
import com.an2t.myapplication.utils.AppConstants
import com.an2t.myapplication.utils.AppConstants.Companion.PERMISSIONS_REQUEST_ACCESS_FINE_LOCATION
import com.an2t.myapplication.utils.UserLocationClient
import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.SupportMapFragment
import com.google.android.gms.maps.model.*
import kotlinx.android.synthetic.main.fragment_maps.*
import kotlinx.coroutines.*
import java.io.IOException
import java.util.*
import kotlin.system.measureTimeMillis

/**
 * A simple [Fragment] subclass.
 * Use the [MapsFragment.newInstance] factory method to
 * create an instance of this fragment.
 */
class MapsFragment : AppCompatDialogFragment(), OnMapReadyCallback, GoogleMap.OnCameraMoveListener,
    GoogleMap.OnCameraIdleListener, UserLocationClient.LocationHelperCallback
    {

    private var mMap: GoogleMap? = null
    private var userLatLng: LatLng? = null
    val job = Job()
    val uiScope = CoroutineScope(Dispatchers.Main + job)
    private val TAG = "AddNewAddressFragment"

    lateinit var binding: FragmentMapsBinding
    var selectedPosition = 0
    var zoomLevel = 13f
    private var locationHelper: UserLocationClient? = null
    private var isForAddressAddition: Boolean = true

    //    private lateinit var addNewAddressViewModel: AddNewAddressViewModel
    private lateinit var userID: String
    private var addressId = ""
    private var isFrom = ""


    private var isEditFromOrderSummary: Boolean = false

    private lateinit var onLocationFetched: OnLocationFetched


    companion object {
        fun newInstance(
            onLocationFetched: OnLocationFetched,
        ) =
            MapsFragment().apply {
                this.onLocationFetched = onLocationFetched
            }
    }


    interface OnLocationFetched {
        fun onLocationFetchedListener()
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
//        return inflater.inflate(R.layout.fragment_maps, container, false)

        binding = FragmentMapsBinding.inflate(inflater, container, false)
        val root: View = binding.root
        return root
    }


    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        setUpMaps()


        binding.imgMyLocation.setOnClickListener {
            requestLocation()
        }

        binding.btnConfirm.setOnClickListener { view->
            this@MapsFragment.onLocationFetched.onLocationFetchedListener()
        }
        setUpUserLocationHelper()
//        showProgress()
//        requestLocation()
    }

    private fun hideProgress() {
        binding.pbShow.visibility = View.GONE
        binding.clContent.visibility = View.VISIBLE
    }

    private fun showProgress() {
        binding.pbShow.visibility = View.VISIBLE
        binding.clContent.visibility = View.GONE
    }


    private fun setUpMaps() {
        val mapFragment = childFragmentManager.findFragmentById(R.id.map) as SupportMapFragment
        mapFragment.getMapAsync(this)
    }


    override fun onMapReady(googleMap: GoogleMap) {
        mMap = googleMap
        mMap?.setOnCameraMoveListener(this)
        mMap?.setOnCameraIdleListener(this)

//        val userAddressResult = arguments?.getParcelable<UserAddressData>(USER_ADDRESS_DATA)
        var latitude = ""
        var longitude = ""

        /** TO UPDATE ADDRESS *//*
        if (!isForAddressAddition) {
            plotMarker(latitude.toString(), longitude.toString())
            return
        }else{
            addNewAddressViewModel.saveUserLatLng(latitude.toString(), longitude.toString())
        }

        val userLatitude = QminSharedPreferences.getString(Constants.USER_LATITUDE) ?: ""
        val userLongitude = QminSharedPreferences.getString(Constants.USER_LONGITUDE) ?: ""*/

        if (latitude.toString().isEmpty() || longitude.toString().isEmpty()) {
            showProgress()
            requestLocation()
        } else {
            plotMarker(latitude.toString(), longitude.toString())
        }
        disableMap()

    }

    private fun setUpUserLocationHelper() {
        locationHelper = UserLocationClient(this)
    }

    private fun requestLocation() {
        context?.let { context ->
            locationHelper?.requestLastKnownLocation(context)
            locationHelper?.startLocationUpdates(context)
        }
    }

    private fun disableMap() {
        if (!isForAddressAddition) {
            mMap!!.uiSettings.isScrollGesturesEnabled = false
            mMap!!.uiSettings.isZoomGesturesEnabled = false
            mMap!!.uiSettings.isScrollGesturesEnabledDuringRotateOrZoom = false
        }
    }


    private fun plotMarker(
        userLatitude: String,
        userLongitude: String
    ) {

//        userAddressResult.latLong = UserLatLong(userLatitude.toDouble(), userLongitude.toDouble())
        val defaultLocationOnMap = LatLng(userLatitude.toDouble(), userLongitude.toDouble())
        val cameraPosition =
            CameraPosition.Builder().target(defaultLocationOnMap).zoom(zoomLevel).build()
        mMap?.animateCamera(CameraUpdateFactory.newCameraPosition(cameraPosition))
    }


    override fun onCameraMove() {
        mMap?.clear()
    }

    override fun onCameraIdle() {
        mMap?.cameraPosition?.target?.let { target ->
            mMap?.cameraPosition?.target?.latitude?.let { latitude ->
                mMap?.cameraPosition?.target?.longitude?.let { longitude ->
                    context?.let { context ->

//                        userAddressResult.latLong = UserLatLong(latitude, longitude)

//                        with(userAddressResult.latLong) {
//                            this?.latitude = latitude
//                            this?.longitude = longitude
//                        }
                        val markerOptions = MarkerOptions().position(target)
                            .icon(
                                bitmapDescriptorFromVector(context, R.drawable.ic_map_pin)
                            )
                        mMap?.addMarker(markerOptions)
                        updateGeoReverseCodedAddress(
                            latitude = latitude,
                            longitude = longitude
                        )
                    }
                }
            }
        }
    }

    private fun bitmapDescriptorFromVector(context: Context, vectorResId: Int): BitmapDescriptor? {
        return ContextCompat.getDrawable(context, vectorResId)?.run {
            setBounds(0, 0, intrinsicWidth, intrinsicHeight)
            val bitmap =
                Bitmap.createBitmap(intrinsicWidth, intrinsicHeight, Bitmap.Config.ARGB_8888)
            draw(Canvas(bitmap))
            BitmapDescriptorFactory.fromBitmap(bitmap)
        }
    }


    private fun updateGeoReverseCodedAddress(latitude: Double, longitude: Double) {
        userLatLng = LatLng(latitude, longitude)
        if (Geocoder.isPresent()) {
            var addressList: List<Address>? = null
            uiScope.launch(Dispatchers.IO) {
                measureTimeMillis {
                    addressList = getReverseGeoLocation(latitude, longitude)
                }
                withContext(Dispatchers.Main) {
                    updateLocationForm(addressList)
                }
            }
        }
    }

    private fun updateLocationForm(
        addressList: List<Address>?
    ) {
        if (addressList?.size != 0) {
            binding.tvShowAddress.text = addressList?.get(0)?.getAddressLine(0).toString()
        }
    }


    private suspend fun getReverseGeoLocation(
        latitude: Double,
        longitude: Double
    ): List<Address>? =
        coroutineScope {
            val geoCoder = Geocoder(context)
            val addressList =
                async {
                    try {
                        geoCoder.getFromLocation(latitude, longitude, 6)
                    } catch (exception: Exception) {
                        null
                    }
                }
            addressList.await()
        }


    /**
     * Request Location
     * */
    private fun requestLocationPermission() {
        requestPermissions(
            arrayOf(Manifest.permission.ACCESS_FINE_LOCATION),
            PERMISSIONS_REQUEST_ACCESS_FINE_LOCATION
        )
    }


    override fun onLocationPermissionNeeded() {
        requestLocationPermission()
    }

    override fun onLocationUpdated(location: Location, isItLastKnownLocation: Boolean) {
        if (isItLastKnownLocation) return

        hideProgress()

        locationHelper?.stopLocationUpdates()
        val addressList: List<Address>
        val geocoder = Geocoder(context, Locale.getDefault())

        plotMarker(location.latitude.toString(), location.longitude.toString())

        val editor = context?.getSharedPreferences(
            AppConstants.SHARED_PREF_DOG_APP,
            AppCompatActivity.MODE_PRIVATE
        )?.edit()
        editor?.putString(AppConstants.LAT, location.latitude.toString())
        editor?.putString(AppConstants.LNG, location.longitude.toString())
        editor?.apply()


        try {
            addressList = geocoder.getFromLocation(
                location.latitude,
                location.longitude, 6
            )
            updateLocationForm(addressList)
        } catch (e: IOException) {
            e.printStackTrace()
        }

    }

    override fun onLocationUpdateFailure(failureReason: UserLocationClient.LocationUpdateFailureReason) {
        activity?.let { activity ->
            locationHelper?.resolveLocationExceptionIfPossible(activity = activity)
        }
    }


}