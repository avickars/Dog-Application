package com.an2t.myapplication.maps

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.appcompat.app.AppCompatDialogFragment
import androidx.fragment.app.DialogFragment
import com.an2t.myapplication.R
import com.an2t.myapplication.databinding.FragmentGalleryOrCameraBinding
import com.an2t.myapplication.databinding.FragmentMapsBinding

class GalleryOrCameraFragment : AppCompatDialogFragment() {

    private lateinit var onGalleryOrCameraSelected: OnGalleryOrCameraSelected

    lateinit var binding: FragmentGalleryOrCameraBinding

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        binding = FragmentGalleryOrCameraBinding.inflate(inflater, container, false)
        val root: View = binding.root
        return root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        binding.tvCamera.setOnClickListener {
            this@GalleryOrCameraFragment.onGalleryOrCameraSelected.onGalleryOrCameraSelectedListener(true)
        }
        binding.tvGallery.setOnClickListener {
            this@GalleryOrCameraFragment.onGalleryOrCameraSelected.onGalleryOrCameraSelectedListener(false)
        }
    }

    companion object {
        fun newInstance(
            onGalleryOrCameraSelected: OnGalleryOrCameraSelected,
        ) =
            GalleryOrCameraFragment().apply {
                this.onGalleryOrCameraSelected = onGalleryOrCameraSelected
            }
    }


    interface OnGalleryOrCameraSelected{
        fun onGalleryOrCameraSelectedListener(isCamera : Boolean)
    }
}