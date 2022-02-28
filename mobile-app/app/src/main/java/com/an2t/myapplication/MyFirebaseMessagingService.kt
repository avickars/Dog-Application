package com.an2t.myapplication

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.ClipDescription
import android.content.Context
import android.content.Intent
import android.os.Build
import android.widget.RemoteViews
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.core.app.RemoteInput
import com.an2t.myapplication.home.HomeActivity
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage

const val CHANNEL_ID = "channel_id"
const val CHANNEL_NAME = "com.an2t.myapplication"

class MyFirebaseMessagingService: FirebaseMessagingService() {

    override fun onMessageReceived(rm: RemoteMessage) {
        super.onMessageReceived(rm)
        if(rm.notification != null){
            val noti = rm.notification
            noti?.title?.let {t->
                noti.body?.let {b->
                    generateNotification(t, b)
                }
            }
        }
    }

    fun getRemoteView(title : String, description: String) : RemoteViews {
        return RemoteViews("com.an2t.myapplication", R.layout.notification)
            .apply{
                setTextViewText(R.id.title,title)
                setTextViewText(R.id.desc,description)
                setImageViewResource(R.id.img_logo,R.drawable.home_purple)
            }
    }

    fun generateNotification(title : String, message: String){
        val intent = Intent(this, HomeActivity::class.java)
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP)

        val pendingIntent = PendingIntent.getActivity(this, 0 , intent, PendingIntent.FLAG_ONE_SHOT)


        val builder = NotificationCompat.Builder(applicationContext, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .setAutoCancel(true)
            .setVibrate(longArrayOf(1000,1000,1000,1000))
            .setOnlyAlertOnce(true)
            .setContentIntent(pendingIntent)
            .setContent(getRemoteView(title, message))
            .setPriority(NotificationCompat.PRIORITY_HIGH)


        val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.O){
            val notificationChannel = NotificationChannel(CHANNEL_ID, CHANNEL_NAME, NotificationManager.IMPORTANCE_HIGH)
            notificationManager.createNotificationChannel(notificationChannel)
        }

        notificationManager.notify(0, builder.build())
    }
}