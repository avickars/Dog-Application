package com.an2t.myapplication.utils

import android.Manifest
import android.annotation.SuppressLint
import android.app.Activity
import android.content.Context
import android.content.IntentSender
import android.location.Location
import android.os.Looper
import com.an2t.myapplication.isPermissionGranted
import com.an2t.myapplication.utils.AppConstants.Companion.REQUEST_CHECK_LOCATION_SETTINGS
import com.google.android.gms.common.api.ResolvableApiException
import com.google.android.gms.location.*
import com.google.android.gms.tasks.Task


/**
 * Helper class to get User's device location updates.
 * @param context Required to access permissions and get instance of FusedLocationProviderClient
 * @param callback LocationHelperCallback needs to be implemented to update the caller about the
 *        states of the location requests made
 *
 */
class UserLocationClient(
    private val callback: LocationHelperCallback
) {

    private val TAG = "UserLocationHelper"
    private var fusedLocationClient: FusedLocationProviderClient? = null


    enum class LocationUpdateFailureReason {
        /* Last Known Location request was successful, but the location returned was null. */
        LAST_KNOWN_LOCATION_NULL,
        PERIODIC_UPDATED_LOCATION_NULL,
        PERIODIC_UPDATED_LOCATION_EMPTY
    }

    fun initFusedLocationClient(context: Context){
        if(fusedLocationClient==null){
            fusedLocationClient = LocationServices.getFusedLocationProviderClient(context)
        }
    }

    /**
     * Call this method to request Last Known Location of the user.
     * It also checks for location permissions in the device.
     * If location request is successful, the method onLocationUpdated is called from the LocationHelperCallback.
     */
    @SuppressLint("MissingPermission")
    fun requestLastKnownLocation(context: Context) {
        //Checking if the app is having any one of the location permissions atleast.
        if (context.isPermissionGranted(Manifest.permission.ACCESS_COARSE_LOCATION)
            ||
            context.isPermissionGranted(Manifest.permission.ACCESS_FINE_LOCATION)
        ) {
            initFusedLocationClient(context)
            fusedLocationClient?.lastLocation
                ?.addOnSuccessListener { location ->
                    if (location != null) {
                        callback.onLocationUpdated(location, true)
                    } else {
                        callback.onLocationUpdateFailure(LocationUpdateFailureReason.LAST_KNOWN_LOCATION_NULL)
                    }
                }
                ?.addOnFailureListener { exception ->
//                    Logger.d(TAG, "Exception accessing Location = ${exception.message}")
                    if (exception is SecurityException) {
                        //If it is a Security Exception the it is because of the permission not granted.
                        callback.onLocationPermissionNeeded()
                    }
                }

        } else (
                callback.onLocationPermissionNeeded()
                )
    }


    private val locationRequest = LocationRequest.create()?.apply {
        interval = 1000
        fastestInterval = 1000
        priority = LocationRequest.PRIORITY_HIGH_ACCURACY
    }


    private val locationCallback = object : LocationCallback() {
        override fun onLocationResult(locationResult: LocationResult?) {
            try{
                if (locationResult == null) {
                    callback.onLocationUpdateFailure(LocationUpdateFailureReason.PERIODIC_UPDATED_LOCATION_NULL)
                } else if (locationResult.locations.isEmpty()) {
                    callback.onLocationUpdateFailure(LocationUpdateFailureReason.PERIODIC_UPDATED_LOCATION_EMPTY)
                } else if (locationResult.locations[0] != null) {
                    if(locationResult.locations.isNotEmpty()){
                        callback.onLocationUpdated(locationResult.locations[0])
                    }
                } else {
                    callback.onLocationUpdateFailure(LocationUpdateFailureReason.PERIODIC_UPDATED_LOCATION_NULL)
                }
            }catch (e : Exception){

            }

        }
    }


    @SuppressLint("MissingPermission")
    fun startLocationUpdates(context: Context) {

        if (context.isPermissionGranted(Manifest.permission.ACCESS_COARSE_LOCATION)
            ||
            context.isPermissionGranted(Manifest.permission.ACCESS_FINE_LOCATION)
        ) {
            initFusedLocationClient(context)
            fusedLocationClient?.requestLocationUpdates(
                locationRequest,
                locationCallback,
                Looper.getMainLooper()
            )
        }
    }

    fun stopLocationUpdates() {
        fusedLocationClient?.removeLocationUpdates(locationCallback)
    }

    fun resolveLocationExceptionIfPossible(activity: Activity) {
        locationRequest?.let { request ->
            val builder = LocationSettingsRequest.Builder()
                .addLocationRequest(request)
            val client: SettingsClient = LocationServices.getSettingsClient(activity)
            val task: Task<LocationSettingsResponse> = client.checkLocationSettings(builder.build())

            task.addOnSuccessListener {
                // All location settings are satisfied. The client can initialize
                // location requests here.
                // ...
//                Logger.d(TAG, "Location is already enabled, some other issue")
            }

            task.addOnFailureListener { exception ->
                if (exception is ResolvableApiException) {
                    // Location settings are not satisfied, but this can be fixed
                    // by showing the user a dialog.
                    try {
                        // Show the dialog by calling startResolutionForResult(),
                        // and check the result in onActivityResult().
                        exception.startResolutionForResult(
                            activity,
                            REQUEST_CHECK_LOCATION_SETTINGS
                        )

                    } catch (sendEx: IntentSender.SendIntentException) {
                        // Ignore the error.
                        sendEx.printStackTrace()

                    }
                }
            }
        }
    }

    /**
     * Interface to provide certain update statuses to the caller regarding the location request
     */
    interface LocationHelperCallback {
        /**
         * This method is called when the permissions needed to access the location is not granted.
         */
        fun onLocationPermissionNeeded()
        /**
         * Called when the requested location update is available and not null.
         */
        fun onLocationUpdated(location: Location, isItLastKnownLocation: Boolean = false)
        /**
         * Current Implementation: The request was successful but the location received was null and hence failed
         * Possible reasons : User has turned off Location Services.
         *                  : Brand new device and location was never updated
         *                  : Google Play services are restarted.
         *        @param failureReason : Enum signifying what was the reason for failure
         */
        fun onLocationUpdateFailure(failureReason: LocationUpdateFailureReason)
    }
}