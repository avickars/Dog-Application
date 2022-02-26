package com.an2t.myapplication.network
import com.an2t.myapplication.model.*
import io.reactivex.Observable
import okhttp3.MultipartBody
import okhttp3.RequestBody
import retrofit2.Call
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.Multipart
import retrofit2.http.POST
import retrofit2.http.Part

interface ServiceAPI {
    @POST("auth/login")
    fun login(@Body user : LoginReq) : Observable<Response<LoginRes>>

    @POST("auth/register")
    fun register(@Body req : RegReq) : Observable<Response<RegRes>>


    @Multipart
    @POST("pets/")
    fun uploadImage(
        @Part image: MultipartBody.Part?,
        @Part("breed") breed: RequestBody,
        @Part("weight") weight: RequestBody,
        @Part("height") height: RequestBody,
        @Part("pet_name") pet_name: RequestBody,
        @Part("refresh_token") refresh_token: RequestBody,
        ) : Call<ImageResponse>
}