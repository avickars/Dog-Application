package com.an2t.myapplication.network
import com.an2t.myapplication.model.*
import com.an2t.myapplication.utils.AppConstants
import io.reactivex.Observable
import okhttp3.MultipartBody
import okhttp3.RequestBody
import retrofit2.Call
import retrofit2.Response
import retrofit2.http.*

interface ServiceAPI {


    @POST("auth/login")
    fun login(@Body user : LoginReq) : Observable<Response<LoginRes>>

    @POST("auth/register")
    fun register(@Body req : RegReq) : Observable<Response<RegRes>>


    @Multipart
    @POST
    fun uploadImage(
        @Url  url: String = AppConstants.BASE_URL_MODEL,
        @Part image: MultipartBody.Part?,
        @Part("lost") lost: RequestBody,
        @Part("refresh_token") refresh_token: RequestBody,
        @Part("lat") lat: RequestBody,
        @Part("lng") lng: RequestBody,
        ) : Call<ImageResponse>

    @POST("pets/getAllUserUploadRecords")
    fun getAllUserUploadRecords(@Body req : CommonReq) : Observable<Response<AllLostUploadRecords>>

    @POST("pets/getAllUserUploadRecordsMap")
    fun getAllUserUploadRecordsForMap(@Body req : CommonReq) : Observable<Response<AllLostUploadRecords>>


    @POST("auth/getUserDataByUserId")
    fun getUserDetails(@Body req : CommonReq) : Observable<Response<UserDetailsResponse>>
}