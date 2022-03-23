package com.an2t.myapplication.maps

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.appcompat.app.AppCompatDialogFragment
import com.an2t.myapplication.R
import com.an2t.myapplication.databinding.FragmentGalleryOrCameraBinding
import com.an2t.myapplication.databinding.FragmentSelectLostOrFoundBinding


class SelectLostOrFoundFragment : AppCompatDialogFragment() {

    private lateinit var onSelectLostOrFound: OnSelectLostOrFound

    lateinit var binding: FragmentSelectLostOrFoundBinding

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        binding = FragmentSelectLostOrFoundBinding.inflate(inflater, container, false)
        val root: View = binding.root
        return root
    }

    companion object {
        fun newInstance(
            onSelectLostOrFound: OnSelectLostOrFound,
        ) =
            SelectLostOrFoundFragment().apply {
                this.onSelectLostOrFound = onSelectLostOrFound
            }
    }


    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        binding.tvFound.setOnClickListener {
            this@SelectLostOrFoundFragment.onSelectLostOrFound.onSelectLostOrFoundListener(0)
        }

        binding.tvLost.setOnClickListener {
            this@SelectLostOrFoundFragment.onSelectLostOrFound.onSelectLostOrFoundListener(1)
        }
    }


    interface OnSelectLostOrFound{
        fun onSelectLostOrFoundListener(uploadType: Int)
    }

}