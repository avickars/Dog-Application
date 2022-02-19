package com.an2t.myapplication.register

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.Toast
import androidx.appcompat.widget.AppCompatEditText
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProviders
import com.an2t.myapplication.R
import com.an2t.myapplication.home.MainActivity
import com.an2t.myapplication.model.LoginReq
import com.an2t.myapplication.model.RegReq

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
                val loginReq = RegReq(device_type, email, password)
                mLVM.callRegisterAPI(loginReq)
            }
        }
    }

    private fun _observe() {
        mLVM.l_res.observe(this,
            Observer { l_res ->
                l_res?.let {
                    if (it.status!!) {
                        val i = Intent(this, MainActivity::class.java)
                        startActivity(i)
                    } else {
                        Toast.makeText(this, it.message, Toast.LENGTH_LONG).show()
                    }
                }
            })
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