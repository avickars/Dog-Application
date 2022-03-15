package com.an2t.myapplication.register

import android.content.Context
import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.Toast
import androidx.appcompat.widget.AppCompatEditText
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProviders
import com.an2t.myapplication.R
import com.an2t.myapplication.home.HomeActivity
import com.an2t.myapplication.model.LoginReq
import com.an2t.myapplication.model.LoginRes
import com.an2t.myapplication.model.RegReq
import com.an2t.myapplication.model.RegRes
import com.an2t.myapplication.utils.AppConstants

class RegisterActivity : AppCompatActivity() {

    lateinit var et_email: AppCompatEditText
    lateinit var et_password: AppCompatEditText
    lateinit var et_password2: AppCompatEditText
    lateinit var btn_login: Button

    lateinit var mLVM: RegisterVM

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_register)
        initViews()
        mLVM = ViewModelProviders.of(this).get(RegisterVM::class.java)
        _addListeners()
        _observe()
    }

    private fun initViews() {
        et_email = findViewById(R.id.et_email)
        et_password = findViewById(R.id.et_password)
        btn_login = findViewById(R.id.btn_login)
        et_password2 = findViewById(R.id.et_password2)
    }

    fun _addListeners(){
        btn_login.setOnClickListener {
            if(validateRegister()){
                val email = et_email.text.toString().trim()
                val password = et_password.text.toString().trim()
                val device_type = "MOBILE"
                val loginReq = RegReq(device_type, email, password, getFCMToken())
                mLVM.callRegisterAPI(loginReq)
            }
        }
    }

    private fun getFCMToken(): String {
        val sharedPreference =
            getSharedPreferences(AppConstants.SHARED_PREF_DOG_APP, Context.MODE_PRIVATE)
        val fcm_t = sharedPreference?.getString(AppConstants.FCM_TOKEN, "")
        return fcm_t!!
    }

    private fun _observe() {
        mLVM.l_res.observe(this,
            Observer { l_res ->
                l_res?.let {
                    if (it.status!!) {
                        saveRefreshToken(it)
                        val i = Intent(this, HomeActivity::class.java)
                        startActivity(i)
                    } else {
                        Toast.makeText(this, it.message, Toast.LENGTH_LONG).show()
                    }
                }
            })
    }

    private fun saveRefreshToken(it: RegRes) {
        val editor = getSharedPreferences(AppConstants.SHARED_PREF_DOG_APP, MODE_PRIVATE).edit()
        editor.putString(AppConstants.REFRESH_TOKEN, it.refreshToken)
        editor.apply()
    }

    fun validateRegister() : Boolean {
        val email = et_email.text.toString().trim()
        val password = et_email.text.toString().trim()
        val password2 = et_password2.text.toString().trim()

        if(email.isEmpty()) {
            et_email.error = "Please enter email id."
            return false
        }
        else if(password.isEmpty()){
            et_password.error = "Please enter password."
            return false
        }
        else if (password2.isEmpty()){
            et_password2.error = "Please enter confirmed password."
            return false
        }
        return true
    }

}