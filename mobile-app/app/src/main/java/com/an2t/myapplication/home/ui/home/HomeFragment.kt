package com.an2t.myapplication.home.ui.home

import android.Manifest
import android.app.Activity
import android.app.ProgressDialog
import android.content.ContentValues
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.provider.MediaStore
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.an2t.myapplication.databinding.FragmentHomeBinding
import com.an2t.myapplication.model.ImageResponse
import com.an2t.myapplication.network.RetrofitClient
import com.an2t.myapplication.network.ServiceAPI
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.http.Part
import java.io.ByteArrayOutputStream

import java.io.File
import java.io.IOException
import java.text.SimpleDateFormat
import java.util.*

//import com.an2t.myapplication.home1.databinding.FragmentHomeBinding
class HomeFragment : Fragment(), Callback<ImageResponse> {

    private var _binding: FragmentHomeBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    internal var cam_photo_path = ""

    // show progress bar in app
    private val file_perm = 2
    internal lateinit var cam_file: File
    internal lateinit var cam_uri_photo: Uri
    internal lateinit var mSAPI: ServiceAPI
    lateinit var mPD: ProgressDialog

    //lateinit var mLVM: MainVM
    lateinit var bitmap: Bitmap


    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        val homeViewModel =
            ViewModelProvider(this).get(HomeViewModel::class.java)

        _binding = FragmentHomeBinding.inflate(inflater, container, false)
        val root: View = binding.root

        iniProgress()
        val btnUploadCamera: Button = binding.btnUploadCamera
        val btnUploadGallery: Button = binding.btnUploadGallery

        btnUploadCamera.setOnClickListener {
            openCamera()
        }
        btnUploadGallery.setOnClickListener {
            openGallery()
        }
        _observe()
        return root
    }

    private fun _observe() {
        mSAPI = RetrofitClient.instance.create(ServiceAPI::class.java)
    }

    private fun iniProgress() {
        mPD = ProgressDialog(activity)
        mPD.setMessage("Uploading Image...")
    }

    fun openGallery() {
        if (Build.VERSION.SDK_INT > Build.VERSION_CODES.M) {
            if (activity?.checkSelfPermission(Manifest.permission.READ_EXTERNAL_STORAGE) == PackageManager.PERMISSION_DENIED) {
                val permission = arrayOf(Manifest.permission.READ_EXTERNAL_STORAGE)
                requestPermissions(permission, 456)
            } else {
                pickImageFromGallery()
            }
        } else {
            pickImageFromGallery()
        }
    }

    fun openCamera() {

        if (Build.VERSION.SDK_INT > Build.VERSION_CODES.M) {
            if (activity?.checkSelfPermission(Manifest.permission.CAMERA) == PackageManager.PERMISSION_DENIED) {
                val permission =
                    arrayOf(Manifest.permission.CAMERA, Manifest.permission.WRITE_EXTERNAL_STORAGE)
                requestPermissions(permission, 222)
            } else {
                pickImageFromCamera()
            }
        } else {
            pickImageFromCamera()
        }
    }

    fun Bitmap.scale(maxWidthAndHeight: Int): Bitmap {
        var newWidth = 0
        var newHeight = 0

        if (this.width >= this.height) {
            val ratio: Float = this.width.toFloat() / this.height.toFloat()

            newWidth = maxWidthAndHeight
            // Calculate the new height for the scaled bitmap
            newHeight = Math.round(maxWidthAndHeight / ratio)
        } else {
            val ratio: Float = this.height.toFloat() / this.width.toFloat()

            // Calculate the new width for the scaled bitmap
            newWidth = Math.round(maxWidthAndHeight / ratio)
            newHeight = maxWidthAndHeight
        }

        return Bitmap.createScaledBitmap(
            this,
            newWidth,
            newHeight,
            false
        )
    }


    private fun pickImageFromCamera() {
        cam_file = createPhotoFile()
        cam_photo_path = cam_file.absolutePath
        var cv = ContentValues()
        cv.put(MediaStore.Images.Media.TITLE, "New Pic")
        cv.put(MediaStore.Images.Media.DESCRIPTION, "done")
        //var uri_photo = FileProvider.getUriForFile(MainActivity@this, "com.binarynumbers.gokozo.fileprovider", cam_file)
        cam_uri_photo = activity?.contentResolver?.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, cv)!!
        val intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
        intent.putExtra(MediaStore.EXTRA_OUTPUT, cam_uri_photo)
        startActivityForResult(intent, 111)
    }


    private fun createPhotoFile(): File {
        val name = SimpleDateFormat("yyyyMMdd_HHmmss").format(Date())
        val storeDir = activity?.getExternalFilesDir(Environment.DIRECTORY_PICTURES)

        try {
            cam_file = File.createTempFile(name, ".jpg", storeDir)
        } catch (e: IOException) {

        }

        //Log.e(TAG, "File " + cam_file.absolutePath)

        return cam_file
    }


    private fun pickImageFromGallery() {
        val intent = Intent(Intent.ACTION_PICK)
        intent.type = "image/*"
        //intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true)
        //intent.action = Intent.ACTION_GET_CONTENT
        startActivityForResult(intent, 123)
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        when (requestCode) {
            456 -> {
                if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    pickImageFromGallery()
                } else {
                    Toast.makeText(
                        activity,
                        "Please enable the permission to upload photos from the gallery",
                        Toast.LENGTH_LONG
                    ).show()
                }
            }
            222 -> {
                if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    pickImageFromCamera()
                } else {
                    Toast.makeText(
                        activity,
                        "Please enable the permission to upload photo from the camera",
                        Toast.LENGTH_LONG
                    ).show()
                }
            }
        }
    }


    private fun shareImageUri(uri: Uri, shareContent: String) {
        val intent = Intent(Intent.ACTION_SEND)
        intent.putExtra(Intent.EXTRA_TEXT, shareContent)
//        intent.type = "text/plain"
        intent.putExtra(Intent.EXTRA_STREAM, uri)
        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        intent.type = "image/png"
        startActivity(intent)
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, intent: Intent?) {
        super.onActivityResult(requestCode, resultCode, intent)
        if (resultCode == Activity.RESULT_OK && requestCode == 123) {
            try {
                bitmap = MediaStore.Images.Media.getBitmap(activity?.contentResolver, intent?.data)
                if (bitmap.height > 1000) {
                    bitmap = bitmap.scale(1000)
                }

                val tempUri = getImageUri()
                val path = ImageFilePath.getPath(activity, tempUri)
                val file = File(path)
                var contentType = ""

                if(!file.name.contains("pdf")){
                    contentType = "image/${file.name.split(".")[1]}"
                }else {
                    contentType = "application/pdf"
                }

                val propertyImage = RequestBody.create(contentType.toMediaTypeOrNull(), file)
                val p = MultipartBody.Part.createFormData("image", file.name, propertyImage)


//                @Part("breed") breed: RequestBody,
//                @Part("weight") weight: RequestBody,
//                @Part("height") height: RequestBody,
//                @Part("pet_name") pet_name: RequestBody,
//                @Part("refresh_token") refresh_token: RequestBody,


                val p1 = RequestBody.create("text/plain".toMediaTypeOrNull(), "bb")
                val p2 = RequestBody.create("text/plain".toMediaTypeOrNull(), "60")
                val p3 = RequestBody.create("text/plain".toMediaTypeOrNull(), "100")
                val p4 = RequestBody.create("text/plain".toMediaTypeOrNull(), "aa")
                val p5 = RequestBody.create("text/plain".toMediaTypeOrNull(), "uMnKWqWzulKYkmEiqBnJQqcQplqaHQ")

                mPD.show()
                mSAPI.uploadImage(
                    p , p1 , p2 , p3 , p4 , p5
                ).enqueue(this)
            } catch (e: IOException) {
                print(e.toString())
            }


        } else if (resultCode == Activity.RESULT_OK && requestCode == 111) {


            try {

                bitmap = MediaStore.Images.Media.getBitmap(activity?.contentResolver, cam_uri_photo)

                if (bitmap.height > 1000) {
                    bitmap = bitmap.scale(1000)
                }

                val tempUri = getImageUri()
                val path = ImageFilePath.getPath(activity, tempUri)
                val file = File(path)
                var contentType = ""
                if(!file.name.contains("pdf")){
                    contentType = "image/${file.name.split(".")[1]}"
                }else {
                    contentType = "application/pdf"
                }

                val propertyImage = RequestBody.create(contentType.toMediaTypeOrNull(), file)
                val p = MultipartBody.Part.createFormData("image", file.name, propertyImage)
                val p1 = RequestBody.create("text/plain".toMediaTypeOrNull(), "bb")
                val p2 = RequestBody.create("text/plain".toMediaTypeOrNull(), "60")
                val p3 = RequestBody.create("text/plain".toMediaTypeOrNull(), "100")
                val p4 = RequestBody.create("text/plain".toMediaTypeOrNull(), "aa")
                val p5 = RequestBody.create("text/plain".toMediaTypeOrNull(), "uMnKWqWzulKYkmEiqBnJQqcQplqaHQ")


                mPD.show()
                mSAPI.uploadImage(
                    p , p1 , p2 , p3 , p4 , p5
                ).enqueue(this)


            } catch (e: IOException) {
                print(e.toString())
            }
        }

    }




    private fun getImageUri(): Uri {
        val bytes = ByteArrayOutputStream()
        bitmap.compress(Bitmap.CompressFormat.JPEG, 5, bytes)
        val path = MediaStore.Images.Media.insertImage(activity?.contentResolver, bitmap, "CameraImage", null)
        return Uri.parse(path)
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

    override fun onResponse(
        call: Call<ImageResponse>,
        response: Response<ImageResponse>
    ) {
        mPD.dismiss()
        val res_data = response.body()
        Toast.makeText(context , "Uploaded " + res_data?.message + " image URL " + res_data?.url, Toast.LENGTH_LONG).show()
    }

    override fun onFailure(call: Call<ImageResponse>, t: Throwable) {
        mPD.dismiss()
        Toast.makeText(context , ""+t.message , Toast.LENGTH_LONG).show()
    }

}