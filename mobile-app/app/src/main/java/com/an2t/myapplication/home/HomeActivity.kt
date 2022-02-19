package com.an2t.myapplication.home

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.text.method.TextKeyListener.clear
import com.google.android.material.bottomnavigation.BottomNavigationView
import androidx.appcompat.app.AppCompatActivity
import androidx.navigation.findNavController
import androidx.navigation.ui.AppBarConfiguration
import androidx.navigation.ui.setupWithNavController
import com.an2t.myapplication.R
import com.an2t.myapplication.databinding.ActivityHomeBinding
import com.an2t.myapplication.login.LoginActivity
import com.an2t.myapplication.model.LoginReq
import com.an2t.myapplication.model.LoginRes
import com.an2t.myapplication.utils.AppConstants

//import com.an2t.myapplication.home1.databinding.ActivityHomeBinding

class HomeActivity : AppCompatActivity() {

    private lateinit var binding: ActivityHomeBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityHomeBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val navView: BottomNavigationView = binding.navView

        val navController = findNavController(R.id.nav_host_fragment_activity_home)
        // Passing each menu ID as a set of Ids because each
        // menu should be considered as top level destinations.
//        val appBarConfiguration = AppBarConfiguration(
//            setOf(
//                R.id.navigation_home, R.id.navigation_dashboard, R.id.navigation_notifications
//            )
//        )
//        setupActionBarWithNavController(navController, appBarConfiguration)
        navView.setupWithNavController(navController)

        _addListeners()
    }


    fun _addListeners(){
        binding.btnLogout.setOnClickListener {
            removeRefreshToken()
            val i = Intent(this, LoginActivity::class.java)
            startActivity(i)
            finish()
        }
    }

    @SuppressLint("CommitPrefEdits")
    private fun removeRefreshToken() {
        val editor = getSharedPreferences(AppConstants.SHARED_PREF_DOG_APP, MODE_PRIVATE).edit()
        editor.apply {
            clear()
            apply()
        }
    }


}