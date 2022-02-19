package com.an2t.myapplication.login

import android.annotation.SuppressLint
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.an2t.myapplication.network.LoginReq
import com.an2t.myapplication.model.LoginRes
import com.an2t.myapplication.network.RetrofitClient
import com.an2t.myapplication.network.ServiceAPI
import io.reactivex.android.schedulers.AndroidSchedulers
import io.reactivex.schedulers.Schedulers

class LoginVM : ViewModel() {

    val l_res = MutableLiveData<LoginRes?>()
    var _s: ServiceAPI

    init {
        val _r = RetrofitClient.instance
        _s = _r.create(ServiceAPI::class.java)
    }

    @SuppressLint("CheckResult")
    fun callLogin(u: LoginReq) {
        _s.login(u)
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

    private fun displayData(p: LoginRes?) {
        l_res.value = p
    }
}