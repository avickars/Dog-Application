package com.an2t.myapplication.utils

import android.util.Log
import com.an2t.myapplication.BuildConfig

object Logger {
    var isEnableLog: Boolean = BuildConfig.DEBUG

    fun d(tag: String?, msg: String?) {
        if (isEnableLog) Log.d(tag, msg!!)
    }

    fun e(tag: String?, msg: String?) {
        if (isEnableLog) Log.e(tag, msg!!)
    }

    fun i(tag: String?, msg: String?) {
        if (isEnableLog) Log.i(tag, msg!!)
    }

    fun v(tag: String?, msg: String?) {
        if (isEnableLog) Log.v(tag, msg!!)
    }

    fun w(tag: String?, msg: String?) {
        if (isEnableLog) Log.w(tag, msg!!)
    }
}
