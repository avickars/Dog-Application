package com.an2t.myapplication.model

import com.google.gson.annotations.SerializedName

data class LoginReq(
    val device_type: String,
    val email: String,
    val password: String
)


data class LoginRes(
    @SerializedName("message")
    val message: String?,
    @SerializedName("refresh_token")
    val refreshToken: String?,
    @SerializedName("status")
    val status: Boolean?
)