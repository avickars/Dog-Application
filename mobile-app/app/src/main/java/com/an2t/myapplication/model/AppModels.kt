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

data class RegReq(
    val device_type: String?,
    val email: String?,
    val password: String?
)

data class RegRes(
    @SerializedName("message")
    val message: String?,
    @SerializedName("refresh_token")
    val refreshToken: String?,
    @SerializedName("status")
    val status: Boolean?
)

data class ImageResponse(
    @SerializedName("outputs")
    val outputs: List<Output>?,
    @SerializedName("status")
    val status: Boolean?,
    @SerializedName("url")
    val url: String?
)


data class Output(
    @SerializedName("boxes")
    val boxes: List<List<Double>>?,
    @SerializedName("labels")
    val labels: List<Double>?,
    @SerializedName("scores")
    val scores: List<Double>?
)