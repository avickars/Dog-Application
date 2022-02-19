package com.an2t.myapplication.register

import android.annotation.SuppressLint
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.an2t.myapplication.model.LoginReq
import com.an2t.myapplication.model.LoginRes
import com.an2t.myapplication.model.RegReq
import com.an2t.myapplication.model.RegRes
import com.an2t.myapplication.network.RetrofitClient
import com.an2t.myapplication.network.ServiceAPI
import io.reactivex.android.schedulers.AndroidSchedulers
import io.reactivex.schedulers.Schedulers

class RegisterVM: ViewModel() {

    val l_res = MutableLiveData<RegRes?>()
    var _s: ServiceAPI

    init {
        val _r = RetrofitClient.instance
        _s = _r.create(ServiceAPI::class.java)
    }

    @SuppressLint("CheckResult")
    fun callRegisterAPI(u: RegReq) {
        _s.register(u)
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