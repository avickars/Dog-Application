package com.an2t.myapplication.home.ui.home.adapters

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.DividerItemDecoration
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.an2t.myapplication.R
import java.util.ArrayList


class MainMatchAdapter() : RecyclerView.Adapter<MainMatchAdapter.MainMatchViewHolder>()  {

    private var mainResList: List<Int>? = null

    fun setListData(notiList: List<Int>) {
        this.mainResList = notiList
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MainMatchViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.match_res_item,parent, false)
        return MainMatchViewHolder(view)
    }

    override fun onBindViewHolder(holder: MainMatchViewHolder, position: Int) {
        // Getting element from names list at this position
        val element = mainResList?.get(position)
        // Updating the text of the txtName with this element
        holder.tv_res_title.text = "App Name"

        var matchResultsAdapter: MatchResultsAdapter

        holder.rv_res.apply {
            layoutManager = LinearLayoutManager(holder.rv_res.context, LinearLayoutManager.HORIZONTAL, false)
            matchResultsAdapter = MatchResultsAdapter()
            adapter = matchResultsAdapter
        }

        val listData = ArrayList<Int>()
        for (i in 1..100) listData.add(1)
        matchResultsAdapter.apply {
            setListData(listData)
            notifyDataSetChanged()
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
    }
}
