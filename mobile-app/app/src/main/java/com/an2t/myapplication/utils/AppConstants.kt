package com.an2t.myapplication.utils

class AppConstants {
    companion object {
        val SHARED_PREF_DOG_APP = "dog-app-storage"
        val REFRESH_TOKEN = "refresh_token"
        val FCM_TOKEN = "fcm_token"
        val BASE_URL_HEROKU = "https://dog-fiinder-all.herokuapp.com/v1/"
        val BASE_URL_MODEL = "http://10.0.0.69:5001/upload"
        val REQUEST_CHECK_LOCATION_SETTINGS = 102
        val PERMISSIONS_REQUEST_ACCESS_FINE_LOCATION = 101
    }
}