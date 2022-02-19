package com.an2t.myapplication.login

import android.R.attr.data
import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.widget.AppCompatEditText
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProviders
import com.an2t.myapplication.R
import com.an2t.myapplication.home.MainActivity


class LoginActivity : AppCompatActivity() {

    lateinit var et_email: AppCompatEditText
    lateinit var et_password: AppCompatEditText
    lateinit var btn_login: Button

    lateinit var mLVM: LoginVM

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        initViews()
        mLVM = ViewModelProviders.of(this).get(LoginVM::class.java)
        _addListeners()
        _observe()
    }

    private fun initViews() {
        et_email = findViewById(R.id.et_email)
        et_password = findViewById(R.id.et_password)
        btn_login = findViewById(R.id.btn_login)
    }

    fun _addListeners(){
        btn_login.setOnClickListener {
            if(validateLogin()){
                Toast.makeText(
                    this, "Call api here",
                    Toast.LENGTH_LONG
                ).show()
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


    fun validateLogin() : Boolean {
        val email = et_email.text.toString().trim()
        val password = et_email.text.toString().trim()

        if(email.isEmpty()) {
            et_email.error = "Please enter email id"
            return false
        }
        else if(password.isEmpty()){
            et_password.error = "Please enter password"
            return false
        }
        return true
    }
}


//        val sharedPref = getPreferences(Context.MODE_PRIVATE)
//        val isNightMode = sharedPref.getBoolean(getString(R.string.is_night_mode), false)
//        switch_btn.isChecked = isNightMode
//
//        if(isNightMode){
//            AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_YES)
//        } else {
//            AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO)
//        }
//
//        switch_btn.setOnCheckedChangeListener{ _, isChecked ->
//            if(isChecked){
//                AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_YES)
//            } else {
//                AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO)
//            }
//            with (sharedPref.edit()) {
//                putBoolean(getString(R.string.is_night_mode), isChecked)
//                apply()
//            }
//        }
//
//        tv_sign_up.setOnClickListener {
//            val intent = Intent(this, RegisterActivity::class.java)
//            startActivity(intent)
//        }
