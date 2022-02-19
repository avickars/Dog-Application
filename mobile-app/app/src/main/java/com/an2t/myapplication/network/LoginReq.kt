package com.an2t.myapplication.network

data class LoginReq(
    val device_type: String,
    val email: String,
    val password: String
)