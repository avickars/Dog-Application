package com.an2t.myapplication.model

import com.google.gson.annotations.SerializedName

data class LoginReq(
    val device_type: String,
    val email: String,
    val password: String,
    val fcm_token: String
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
    val password: String?,
    val fcm_token: String
)

data class CommonReq(
    val refresh_token: String?,
    val fcm_token: String
)


data class NotificationResponse(
    val title: String,
    val message: String,
    val ac_img: String,
    val m_img: String
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

data class AllLostUploadRecords(
    @SerializedName("match_list")
    val matchList: List<Match>?,
    @SerializedName("status")
    val status: Boolean?
)

data class FinalOutput(
    @SerializedName("c_score")
    val cScore: Double?,
    @SerializedName("id")
    val id: Int?,
    @SerializedName("image_url")
    val imageUrl: String?,
    @SerializedName("user_id")
    val userId: Int?
)

data class Match(
    @SerializedName("final_output")
    val finalOutput: List<FinalOutput>?,
    @SerializedName("image_url")
    val imageUrl: String?,
    @SerializedName("is_lost")
    val isLost: Int?,
    @SerializedName("user_id")
    val userId: Int?
)