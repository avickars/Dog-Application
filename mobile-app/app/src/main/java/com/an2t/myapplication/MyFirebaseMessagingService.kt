package com.an2t.myapplication

import android.annotation.SuppressLint
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.graphics.BitmapFactory
import android.os.Build
import android.widget.RemoteViews
import androidx.core.app.NotificationCompat
import com.an2t.myapplication.home.HomeActivity
import com.an2t.myapplication.model.NotificationResponse
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage
import java.net.URL


const val CHANNEL_ID = "channel_id"
const val CHANNEL_NAME = "com.an2t.myapplication"

class MyFirebaseMessagingService: FirebaseMessagingService() {

    override fun onMessageReceived(rm: RemoteMessage) {
        super.onMessageReceived(rm)
        rm.data.values.let {
            val l = rm.data.values.toList()
            val n_res =
                NotificationResponse(l[0], l[2], l[1], l[3])
            generateNotification(n_res)
        }
    }

    @SuppressLint("RemoteViewLayout")
    fun getRemoteView(n_res: NotificationResponse) : RemoteViews {

        val rv = RemoteViews("com.an2t.myapplication", R.layout.notification)

        val ac_img = URL(n_res.ac_img)
        val ac_bit = BitmapFactory.decodeStream(ac_img.openConnection().getInputStream())

        val match_img = URL(n_res.m_img)
        val match_bit = BitmapFactory.decodeStream(match_img.openConnection().getInputStream())

        rv.apply{
            setTextViewText(R.id.title,n_res.title)
            setTextViewText(R.id.desc,n_res.message)
            setImageViewBitmap(R.id.img_logo, ac_bit)
            setImageViewBitmap(R.id.img_match, match_bit)
        }
        return rv

    }

    fun generateNotification(n_res : NotificationResponse){
        val intent = Intent(this, HomeActivity::class.java)
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP)

        val pendingIntent = PendingIntent.getActivity(this, 0 , intent, PendingIntent.FLAG_ONE_SHOT)


        val builder = NotificationCompat.Builder(applicationContext, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .setAutoCancel(true)
            .setVibrate(longArrayOf(1000,1000,1000,1000))
            .setOnlyAlertOnce(true)
            .setContentIntent(pendingIntent)
            .setCustomContentView(getRemoteView(n_res))
            .setCustomBigContentView(getRemoteView(n_res))
            .setPriority(NotificationCompat.PRIORITY_HIGH)


        val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.O){
            val notificationChannel = NotificationChannel(CHANNEL_ID, CHANNEL_NAME, NotificationManager.IMPORTANCE_HIGH)
            notificationManager.createNotificationChannel(notificationChannel)
        }

        notificationManager.notify(0, builder.build())
    }
}