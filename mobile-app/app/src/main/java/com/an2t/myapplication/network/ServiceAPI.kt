package com.an2t.myapplication.network
import com.an2t.myapplication.model.LoginRes
import io.reactivex.Observable
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.POST

interface ServiceAPI {
    @POST("auth/login")
    fun login(@Body user : LoginReq) : Observable<Response<LoginRes>>

//    @POST("auth/register")
//    fun register(@Body req : MapsReq) : Observable<MapsRes>

}