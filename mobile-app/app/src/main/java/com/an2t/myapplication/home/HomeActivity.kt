package com.an2t.myapplication.home

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import com.google.android.material.bottomnavigation.BottomNavigationView
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AppCompatDialogFragment
import androidx.fragment.app.Fragment
import androidx.navigation.findNavController
import androidx.navigation.ui.setupWithNavController
import com.an2t.myapplication.maps.MapsFragment
import com.an2t.myapplication.R
import com.an2t.myapplication.databinding.ActivityHomeBinding
import com.an2t.myapplication.login.LoginActivity
import com.an2t.myapplication.utils.AppConstants
import com.an2t.myapplication.utils.FragmentsTransactionListener

//import com.an2t.myapplication.home1.databinding.ActivityHomeBinding

class HomeActivity : AppCompatActivity(), FragmentsTransactionListener {

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
//        _openMapsBottomSheet()
    }

    private fun _openMapsBottomSheet() {
        val bottomSheetFragment = MapsFragment()
        bottomSheetFragment.isCancelable = false
        openBottomSheetFragment(bottomSheetFragment)
    }


    fun _addListeners(){
        binding.btnLogout.setOnClickListener {
            removeRefreshToken()
            val i = Intent(this, LoginActivity::class.java)
            startActivity(i)
            finish()
        }

        binding.card.setOnClickListener {
            _openMapsBottomSheet()
        }

    }

    @SuppressLint("CommitPrefEdits")
    private fun removeRefreshToken() {
        val editor = getSharedPreferences(AppConstants.SHARED_PREF_DOG_APP, MODE_PRIVATE).edit()
        editor.apply {
            remove(AppConstants.REFRESH_TOKEN)
            apply()
        }
    }


    override fun openBottomSheetFragment(fragment: AppCompatDialogFragment) {
        try {
            if (!supportFragmentManager.isDestroyed) {
                this.let {
                    supportFragmentManager.let {
                        fragment.show(
                            it,
                            fragment.tag
                        )
                    }
                }
            }
        } catch (e: IllegalStateException) {
        }
    }


    override fun addReplaceFragment(
        fragment: Fragment,
        isReplaceFragment: Boolean,
        addToBackStack: Boolean,
        tag: String
    ) {
        val fragmentTransaction = supportFragmentManager.beginTransaction()
        if (isReplaceFragment) {
            fragmentTransaction.replace(R.id.container, fragment)
        } else {
            fragmentTransaction.add(R.id.container, fragment)
        }
        if (addToBackStack) {
            fragmentTransaction.addToBackStack(tag)
        }
        fragmentTransaction.commit()
        //intent.removeExtra(Constants.CARTID)
    }


    override fun dismissBottomSheetFragment(fragment: AppCompatDialogFragment) {
        fragment.dismiss()
    }

}