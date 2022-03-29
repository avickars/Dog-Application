package com.an2t.myapplication.home.ui.home.adapters

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.an2t.myapplication.R
import com.an2t.myapplication.model.FinalOutput
import com.squareup.picasso.Picasso


class MatchResultsAdapter(val matchResList: List<FinalOutput>) : RecyclerView.Adapter<MatchResultsAdapter.MatchResultsViewHolder>()  {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MatchResultsViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.match_res_sub_item,parent, false)
        return MatchResultsViewHolder(view)
    }

    override fun onBindViewHolder(holder: MatchResultsViewHolder, position: Int) {
        // Getting element from names list at this position
        val o = matchResList.get(position)
        // Updating the text of the txtName with this element
        holder.tv_title_res.visibility = View.GONE
        holder.tv_title_res.text = String.format("%.3f", o.cScore)
        Picasso.get()
            .load(o.imageUrl)
            .placeholder(R.drawable.gallery)
            .error(R.drawable.gallery)
            .into(holder.iv_match_img)

//        Adding an OnClickLister to the holder.itemView
//        holder.itemView.setOnClickListener {
//            // Invoking itemClickListener and passing it the position and name
//            itemClickListener?.invoke(position, element)
//        }
    }

    override fun getItemCount(): Int {
        if (matchResList == null) return 0
        return matchResList?.size
    }


    class MatchResultsViewHolder(view : View): RecyclerView.ViewHolder(view) {
        val iv_match_img = view.findViewById(R.id.iv_match_img) as ImageView
        val tv_title_res = view.findViewById(R.id.tv_title_res) as TextView
    }
}
