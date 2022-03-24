package com.an2t.myapplication.home.ui.home.adapters

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.an2t.myapplication.R
import com.an2t.myapplication.model.Match
import com.squareup.picasso.Picasso


class MainMatchAdapter() : RecyclerView.Adapter<MainMatchAdapter.MainMatchViewHolder>()  {

    private var mainResList: List<Match>? = null

    fun setListData(notiList: List<Match>) {
        this.mainResList = notiList
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MainMatchViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.match_res_item,parent, false)
        return MainMatchViewHolder(view)
    }

    override fun onBindViewHolder(holder: MainMatchViewHolder, position: Int) {
        // Getting element from names list at this position
        val o = mainResList?.get(position)
        // Updating the text of the txtName with this element
//        holder.tv_res_title.text = o?.imageUrl

        Picasso.get()
            .load(o?.imageUrl)
            .placeholder(R.drawable.gallery)
            .error(R.drawable.gallery)
            .into(holder.iv_img_main_dog)


        var matchResultsAdapter: MatchResultsAdapter
        o?.finalOutput?.let {

            val lm =  GridLayoutManager(
                holder.rv_res.context, // context
                3, // span count
                RecyclerView.VERTICAL, // orientation
                false // reverse layout
            )
//            val lm = LinearLayoutManager(holder.rv_res.context, LinearLayoutManager.HORIZONTAL, false)
//            lm.reverseLayout = true
//            lm.stackFromEnd = true
            holder.rv_res.apply {
                layoutManager = lm
                matchResultsAdapter = MatchResultsAdapter(it)
                adapter = matchResultsAdapter
            }
        }
        // Adding an OnClickLister to the holder.itemView
        holder.itemView.setOnClickListener {
            // Invoking itemClickListener and passing it the position and name
//            itemClickListener?.invoke(position, element)
        }
    }

    override fun getItemCount(): Int {
        if (mainResList == null) return 0
        return mainResList?.size!!
    }


    class MainMatchViewHolder(view : View): RecyclerView.ViewHolder(view) {
        val tv_res_title = view.findViewById(R.id.tv_res_title) as TextView
        val rv_res = view.findViewById(R.id.rv_res) as RecyclerView
        val iv_img_main_dog = view.findViewById(R.id.iv_img_main_dog) as ImageView
    }
}
