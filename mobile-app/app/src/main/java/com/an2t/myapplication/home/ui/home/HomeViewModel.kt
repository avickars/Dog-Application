package com.an2t.myapplication.home.ui.home

import android.annotation.SuppressLint
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.an2t.myapplication.model.AllLostUploadRecords
import com.an2t.myapplication.model.CommonReq
import com.an2t.myapplication.model.LoginReq
import com.an2t.myapplication.model.LoginRes
import com.an2t.myapplication.network.RetrofitClient
import com.an2t.myapplication.network.ServiceAPI
import io.reactivex.android.schedulers.AndroidSchedulers
import io.reactivex.schedulers.Schedulers

class HomeViewModel : ViewModel() {

    val l_res = MutableLiveData<AllLostUploadRecords?>()
    var _s: ServiceAPI

    init {
        val _r = RetrofitClient.instance
        _s = _r.create(ServiceAPI::class.java)
    }

    @SuppressLint("CheckResult")
    fun callMatchRecords(token: String, fcm_token: String) {
        _s.getAllUserUploadRecords(CommonReq(token,fcm_token))
            .subscribeOn(Schedulers.io())
            .observeOn(AndroidSchedulers.mainThread())
            .subscribe (
                {res ->
                    when (res.code()) {
                        200 -> {
                            l_res.value = res.body()
                        }
                        else -> {
                        }
                    }
                }, {e ->
                    print(e)
                })
    }

}