package com.an2t.myapplication.network


import com.an2t.myapplication.utils.AppConstants.Companion.BASE_URL_HEROKU

import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.adapter.rxjava2.RxJava2CallAdapterFactory
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

object RetrofitClient {
    private var ourInstance : Retrofit? = null
    val instance : Retrofit
        get() {
            if(ourInstance == null){
                val _c = OkHttpClient().newBuilder()
                    .addInterceptor(HttpLoggingInterceptor().apply {
                        level = HttpLoggingInterceptor.Level.BODY
                    })
                    .readTimeout(60, TimeUnit.SECONDS)
                    .connectTimeout(60, TimeUnit.SECONDS)
                    .build()

                ourInstance = Retrofit.Builder()
                    .baseUrl(BASE_URL_HEROKU)
                    .client(_c)
                    .addConverterFactory(GsonConverterFactory.create())
                    .addCallAdapterFactory(RxJava2CallAdapterFactory.create())
                    .build()
            }
            return ourInstance!!
        }
}