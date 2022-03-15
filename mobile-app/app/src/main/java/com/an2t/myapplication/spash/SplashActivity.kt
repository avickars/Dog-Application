package com.an2t.myapplication.spash

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.os.Handler
import androidx.appcompat.app.AppCompatActivity
import com.an2t.myapplication.R
import com.an2t.myapplication.home.HomeActivity
import com.an2t.myapplication.login.LoginActivity
import com.an2t.myapplication.model.LoginRes
import com.an2t.myapplication.utils.AppConstants.Companion.FCM_TOKEN
import com.an2t.myapplication.utils.AppConstants.Companion.REFRESH_TOKEN
import com.an2t.myapplication.utils.AppConstants.Companion.SHARED_PREF_DOG_APP
import com.google.firebase.iid.FirebaseInstanceId
import com.google.firebase.iid.InstanceIdResult


class SplashActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_splash)
        val sharedPreference =  getSharedPreferences(SHARED_PREF_DOG_APP, Context.MODE_PRIVATE)
        val refresh_token = sharedPreference.getString(REFRESH_TOKEN,"")
        val handler = Handler()


        FirebaseInstanceId.getInstance().instanceId.addOnSuccessListener(
            this
        ) { instanceIdResult: InstanceIdResult ->
            val newToken = instanceIdResult.token
            saveFCMToken(newToken)
            handler.postDelayed(
                Runnable {
                    refresh_token?.let {
                        if(it.isEmpty()){
                            val i = Intent(this, LoginActivity::class.java)
                            startActivity(i)
                            finish()
                        }else{
                            val i = Intent(this, HomeActivity::class.java)
                            startActivity(i)
                            finish()
                        }
                    }
                }, 2000)
        }
    }

    private fun saveFCMToken(fcm_token: String) {
        val editor = getSharedPreferences(SHARED_PREF_DOG_APP, MODE_PRIVATE).edit()
        editor.putString(FCM_TOKEN, fcm_token)
        editor.apply()
    }
}