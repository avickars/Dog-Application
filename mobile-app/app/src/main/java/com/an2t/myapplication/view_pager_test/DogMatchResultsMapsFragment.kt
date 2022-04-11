package com.an2t.myapplication.view_pager_test

import android.content.ActivityNotFoundException
import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.LinearLayoutManager
import com.an2t.myapplication.R
import com.an2t.myapplication.databinding.FragmentDogMatchResultsMapsBinding
import com.an2t.myapplication.home.ui.dashboard.DashboardFragment
import com.an2t.myapplication.home.ui.home.adapters.DashMatchResultsAdapter
import com.an2t.myapplication.model.FinalOutput
import com.an2t.myapplication.model.Match
import com.squareup.picasso.Picasso


// TODO: Rename parameter arguments, choose names that match
// the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
private const val DOG_DATA = "DOG_DATA"
private const val ITEM_NUMBER = "ITEM_NUMBER"


class DogMatchResultsMapsFragment : Fragment() {


    var  onMatchResultClickListener : OnMatchedResListener? = null

    interface OnMatchedResListener{
        fun onMatchedResClick(finalOutput: FinalOutput, itemNumber: Int)
    }

    override fun onAttach(context: Context) {
        super.onAttach(context)
        try {
            val _fc = requireActivity().supportFragmentManager.fragments[0].childFragmentManager.fragments[0]
            if (_fc is OnMatchedResListener) {
                onMatchResultClickListener =  _fc as DashboardFragment
            } else {
                throw ClassCastException(
                    "DashboardFragment must implement OnMatchedResListener"
                )
            }
        } catch (exception: Exception) {
            print(exception.toString())
        }

    }


    private var dogData: Match? = null
    private var itemNumber: Int = 0
    private var selectedEmail: String = ""

    private var _binding: FragmentDogMatchResultsMapsBinding? = null

    private val binding get() = _binding!!

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        arguments?.let {
            dogData = it.getParcelable(DOG_DATA)
            itemNumber = it.getInt(ITEM_NUMBER)
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
        fun newInstance(dogData: Match, itemNumber: Int) =
            DogMatchResultsMapsFragment().apply {
                arguments = Bundle().apply {
                    putParcelable(DOG_DATA, dogData)
                    putInt(ITEM_NUMBER, itemNumber)
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
            lm.reverseLayout = false
            lm.stackFromEnd = false
            binding.rvRes.apply {
                layoutManager = lm
                matchResultsAdapter = DashMatchResultsAdapter(it, DashMatchResultsAdapter.OnClickListener { fo ->
                    binding.llDisDur.visibility = View.VISIBLE
                    binding.cardRes2.visibility = View.VISIBLE
                    binding.tvTitleMatch.visibility = View.VISIBLE
                    binding.tvTitleEmail.visibility = View.VISIBLE
                    selectedEmail = fo.contact_email.toString()
                    binding.tvTitleEmail.text = "Contact Email: ${selectedEmail}"
                    Picasso.get()
                        .load(fo.imageUrl)
                        .placeholder(R.drawable.gallery)
                        .error(R.drawable.gallery)
                        .into(binding.ivImgMainDog2)
                    onMatchResultClickListener?.onMatchedResClick(fo, it.indexOf(fo))
                })
                adapter = matchResultsAdapter
            }
        }


        binding.tvTitleEmail.setOnClickListener {
            val i = Intent(Intent.ACTION_SEND)
            i.type = "message/rfc822"
            i.putExtra(Intent.EXTRA_EMAIL, arrayOf(selectedEmail))
            i.putExtra(Intent.EXTRA_SUBJECT, "subject of email")
            i.putExtra(Intent.EXTRA_TEXT, "body of email")
            try {
                startActivity(Intent.createChooser(i, "Send mail..."))
            } catch (ex: ActivityNotFoundException) {
                Toast.makeText(
                    activity,
                    "There are no email clients installed.",
                    Toast.LENGTH_SHORT
                ).show()
            }
        }


        if(dogData?.isLost == 1){
            binding.tvLostFound.text = resources.getText(R.string.lost_dog_image)
        }else{
            binding.tvLostFound.text = resources.getText(R.string.found_dog_image)
        }
    }

    fun updateDurationAndDistance(distance: String, duration: String) {
        binding.tvDistance.text = "Distance: ${distance}"
        binding.tvDuration.text = "Duration: ${duration}"
        binding.tvBreed.text = "Breed: ${dogData?.breed}"
    }
}