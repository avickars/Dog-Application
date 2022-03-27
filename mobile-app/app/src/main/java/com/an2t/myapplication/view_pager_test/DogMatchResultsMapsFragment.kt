package com.an2t.myapplication.view_pager_test

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.LinearLayoutManager
import com.an2t.myapplication.R
import com.an2t.myapplication.databinding.FragmentDashboardBinding
import com.an2t.myapplication.databinding.FragmentDogMatchResultsMapsBinding
import com.an2t.myapplication.home.ui.home.adapters.DashMatchResultsAdapter
import com.an2t.myapplication.model.Match
import com.squareup.picasso.Picasso

// TODO: Rename parameter arguments, choose names that match
// the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
private const val DOG_DATA = "DOG_DATA"


class DogMatchResultsMapsFragment : Fragment() {
    private var dogData: Match? = null

    private var _binding: FragmentDogMatchResultsMapsBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        arguments?.let {
            dogData = it.getParcelable(DOG_DATA)
        }
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        _binding = FragmentDogMatchResultsMapsBinding.inflate(inflater, container, false)
        val root: View = binding.root
        return root
    }

    companion object {
        @JvmStatic
        fun newInstance(dogData: Match) =
            DogMatchResultsMapsFragment().apply {
                arguments = Bundle().apply {
                    putParcelable(DOG_DATA, dogData)
                }
            }
    }


    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        Picasso.get()
            .load(dogData?.imageUrl)
            .placeholder(R.drawable.gallery)
            .error(R.drawable.gallery)
            .into(binding.ivImgMainDog)


        var matchResultsAdapter: DashMatchResultsAdapter
        dogData?.finalOutput?.let {
            val lm = LinearLayoutManager(requireContext(), LinearLayoutManager.HORIZONTAL, false)
            lm.reverseLayout = true
            lm.stackFromEnd = true
            binding.rvRes.apply {
                layoutManager = lm
                matchResultsAdapter = DashMatchResultsAdapter(it)
                adapter = matchResultsAdapter
            }
        }
    }
}