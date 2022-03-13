package com.an2t.myapplication.utils

class AppConstants {
    companion object {
        val SHARED_PREF_DOG_APP = "dog-app-storage"
        val REFRESH_TOKEN = "refresh_token"
        val BASE_URL_HEROKU = "https://dog-finder-app-1.herokuapp.com/v1/"
        val BASE_URL_EC2 = "http://52.27.29.173:5000/v1/"
        val BASE_URL_LOCAL = "http://192.75.240.60:5000/v1/"
//        flask run --host=192.75.240.33
    }
}