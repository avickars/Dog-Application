package com.an2t.myapplication.home.ui.notifications

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.an2t.myapplication.R

class NotificationAdapter() : RecyclerView.Adapter<NotificationAdapter.NotificationViewHolder>()  {

    private var notiList: List<Int>? = null

    fun setListData(notiList: List<Int>) {
        this.notiList = notiList

    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): NotificationViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.notification_item,parent, false)
        return NotificationViewHolder(view)
    }

    override fun onBindViewHolder(holder: NotificationViewHolder, position: Int) {

    }

    override fun getItemCount(): Int {
        if (notiList == null) return 0
        return notiList?.size!!
    }


    class NotificationViewHolder(view : View): RecyclerView.ViewHolder(view) {
        fun bind(){

        }
    }
}