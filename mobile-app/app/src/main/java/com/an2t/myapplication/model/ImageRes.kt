package com.an2t.myapplication.model


import com.google.gson.annotations.SerializedName

data class ImageRes(
    @SerializedName("message")
    val message: String?,
    @SerializedName("status")
    val status: Boolean?
)