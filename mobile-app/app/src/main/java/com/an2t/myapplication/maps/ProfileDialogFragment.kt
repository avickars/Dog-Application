package com.an2t.myapplication.maps

import android.app.Activity
import android.content.Context
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.appcompat.app.AppCompatDialogFragment
import com.an2t.myapplication.R
import com.an2t.myapplication.databinding.FragmentProfileDialogBinding
import com.an2t.myapplication.utils.AppConstants


class ProfileDialogFragment : AppCompatDialogFragment() {

    lateinit var binding: FragmentProfileDialogBinding
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
    }

    private lateinit var onSignOutClick: OnSignOutClick

    override fun onResume() {
        super.onResume()
        val width = resources.getDimensionPixelSize(R.dimen.profile_dialog_width)
        val height = resources.getDimensionPixelSize(R.dimen.profile_dialog_height)
        dialog!!.window!!.setLayout(width, height)
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        binding = FragmentProfileDialogBinding.inflate(inflater, container, false)
        val root: View = binding.root
        return root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        setEmailName()
        binding.btnSignOut.setOnClickListener {
            dismiss()
            onSignOutClick.onSignOutClickListener()
        }
    }


    private fun setEmailName() {
        val email = getUserEmail()
        if(email.isNotEmpty()){
            binding.tvInitEmail.text = email[0].toString().uppercase()
            binding.tvEmail.text = email
        }
    }

    private fun getUserEmail(): String {
        val sharedPreference =
            context?.getSharedPreferences(AppConstants.SHARED_PREF_DOG_APP, Context.MODE_PRIVATE)
        val email = sharedPreference?.getString(AppConstants.USER_EMAIL, "")
        return email!!
    }

    override fun onAttach(activity: Activity) {
        super.onAttach(activity)
        try {
            onSignOutClick = activity as OnSignOutClick
        } catch (e: ClassCastException) {
            throw ClassCastException("$activity must implement OnSignOutClick")
        }
    }

    interface OnSignOutClick{
        fun onSignOutClickListener()
    }
}