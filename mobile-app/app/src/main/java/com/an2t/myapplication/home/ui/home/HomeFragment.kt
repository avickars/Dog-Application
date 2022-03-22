package com.an2t.myapplication.home.ui.home

import android.Manifest
import android.app.Activity
import android.app.PendingIntent
import android.app.ProgressDialog
import android.content.ContentValues
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.provider.MediaStore
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ProgressBar
import android.widget.Toast
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import com.an2t.myapplication.R
import com.an2t.myapplication.databinding.FragmentHome1Binding
import com.an2t.myapplication.home.HomeActivity
import com.an2t.myapplication.home.ui.home.adapters.MainMatchAdapter
import com.an2t.myapplication.model.ImageResponse
import com.an2t.myapplication.model.Output
import com.an2t.myapplication.network.RetrofitClient
import com.an2t.myapplication.network.ServiceAPI
import com.an2t.myapplication.utils.AppConstants
import com.an2t.myapplication.utils.AppConstants.Companion.BASE_URL_MODEL
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import java.io.File
import java.io.IOException
import java.text.SimpleDateFormat
import java.util.*


//import com.an2t.myapplication.home1.databinding.FragmentHomeBinding
class HomeFragment : Fragment(), Callback<ImageResponse> {

    private var _binding: FragmentHome1Binding? = null

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
    lateinit var mPB_show: ProgressBar

    lateinit var bitmap: Bitmap

    private lateinit var matchResultsAdapter: MainMatchAdapter

    private lateinit var homeViewModel:HomeViewModel


    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        homeViewModel =
            ViewModelProvider(this).get(HomeViewModel::class.java)

        _binding = FragmentHome1Binding.inflate(inflater, container, false)
        val root: View = binding.root

        iniProgress()
        val btnUploadCamera: Button = binding.btnUploadCamera
        val btnUploadGallery: Button = binding.btnUploadGallery
        mPB_show = binding.pbShow
//        animationView = binding.animationView
//        imageUploaded = binding.imgUpload
//        d_op = binding.imgDOp
//        tv_data = binding.tvData

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

        homeViewModel.l_res.observe(viewLifecycleOwner) {
            l_res ->
            l_res?.status?.let {
                hideProgress()
                if(it){
                    l_res.matchList?.let {
                        matchResultsAdapter.apply {
                            setListData(it)
                            notifyDataSetChanged()
                        }
                    }
                }
            }
        }


        homeViewModel.show_err.observe(viewLifecycleOwner) {
                message ->
            hideProgress()
            Toast.makeText(
                activity,
                message.toString(),
                Toast.LENGTH_LONG
            ).show()
        }
    }

    private fun iniProgress() {
        mPD = ProgressDialog(activity)
        mPD.setMessage("Uploading Image...")
    }


    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        showProgress()
        _binding?.rvShowMatchResults!!.apply {
            layoutManager = LinearLayoutManager(activity)
//            val decoration = DividerItemDecoration(activity, DividerItemDecoration.VERTICAL)
//            addItemDecoration(decoration)
            matchResultsAdapter = MainMatchAdapter()
            adapter = matchResultsAdapter
        }

        val refresh_token = getRefreshToken()
        val fcm_token = getFCMToken()
        homeViewModel.callMatchRecords(refresh_token, fcm_token)
    }

    private fun hideProgress() {
        mPB_show.visibility = View.GONE
        _binding?.rvShowMatchResults?.visibility = View.VISIBLE
    }

    private fun showProgress() {
        mPB_show.visibility = View.VISIBLE
        _binding?.rvShowMatchResults?.visibility = View.GONE
    }

    private fun getFCMToken(): String {
        val sharedPreference =
            activity?.getSharedPreferences(AppConstants.SHARED_PREF_DOG_APP, Context.MODE_PRIVATE)
        val fcm_t = sharedPreference?.getString(AppConstants.FCM_TOKEN, "")
        return fcm_t!!
    }

    private fun getRefreshToken(): String {
        val sharedPreference =
            activity?.getSharedPreferences(AppConstants.SHARED_PREF_DOG_APP, Context.MODE_PRIVATE)
        val refresh_token = sharedPreference?.getString(AppConstants.REFRESH_TOKEN, "")
        return refresh_token!!
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

                intent?.data?.let {
                    uri ->
                    val path = ImageFilePath.getPath(activity, uri)
                    val file = File(path)
                    var contentType = ""

                    if(!file.name.contains("pdf")){
                        contentType = "image/${file.name.split(".")[1]}"
                    }else {
                        contentType = "application/pdf"
                    }
                    val refresh_token = getRefreshToken()
                    val propertyImage = RequestBody.create(contentType.toMediaTypeOrNull(), file)
                    val p = MultipartBody.Part.createFormData("image", file.name, propertyImage)

                    val p1 = RequestBody.create("text/plain".toMediaTypeOrNull(), "1")
                    val p2 = RequestBody.create("text/plain".toMediaTypeOrNull(), refresh_token)

                    mPD.show()
                    mSAPI.uploadImage(
                        BASE_URL_MODEL,
                        p , p1 , p2
                    ).enqueue(this)
                }
//                val selectedImageUri: Uri = intent?.data
//                bitmap = MediaStore.Images.Media.getBitmap(activity?.contentResolver, intent?.data)
//                MediaStore.Images.Media.get
//                if (bitmap.height > 1000) {
//                    bitmap = bitmap.scale(1000)
//                }

//                val tempUri = getImageUri()

            } catch (e: IOException) {
                print(e.toString())
            }


        } else if (resultCode == Activity.RESULT_OK && requestCode == 111) {


            try {

                bitmap = MediaStore.Images.Media.getBitmap(activity?.contentResolver, cam_uri_photo)

                if (bitmap.height > 1000) {
                    bitmap = bitmap.scale(1000)
                }

//                val tempUri = getImageUri()
                val path = ImageFilePath.getPath(activity, cam_uri_photo)
                val file = File(path)
                var contentType = ""
                if(!file.name.contains("pdf")){
                    contentType = "image/${file.name.split(".")[1]}"
                }else {
                    contentType = "application/pdf"
                }
                val refresh_token = getRefreshToken()
                val propertyImage = RequestBody.create(contentType.toMediaTypeOrNull(), file)
                val p = MultipartBody.Part.createFormData("image", file.name, propertyImage)
                val p1 = RequestBody.create("text/plain".toMediaTypeOrNull(), "1")
                val p2 = RequestBody.create("text/plain".toMediaTypeOrNull(), refresh_token)


//                d_op.visibility = View.VISIBLE
//                animationView.visibility = View.GONE

                mPD.show()
                mSAPI.uploadImage(
                    BASE_URL_MODEL,
                    p , p1,p2
                ).enqueue(this)


            } catch (e: IOException) {
                print(e.toString())
            }
        }

    }



//    @Deprecated
//    private fun getImageUri(): Uri {
//        val bytes = ByteArrayOutputStream()
//        bitmap.compress(Bitmap.CompressFormat.JPEG, 5, bytes)
//        val path = MediaStore.Images.Media.insertImage(activity?.contentResolver, bitmap, "CameraImage", null)
//        return Uri.parse(path)
//    }

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

        res_data?.status?.let {
            Toast.makeText(context , "Your request has been submtited successfully. We ll get back to you with results in some time." , Toast.LENGTH_LONG).show()
        }
    }

    override fun onFailure(call: Call<ImageResponse>, t: Throwable) {
        mPD.dismiss()
        Toast.makeText(context , ""+t.message , Toast.LENGTH_LONG).show()
    }


    private val CHANNEL_ID = "channel_id_example_01"
    private val notificationId = 101

    private fun sendNotification(img_url: Bitmap?, outputs: List<Output>?) {
        context?.let {
            val intent = Intent(activity, HomeActivity::class.java).apply {
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
            }

            val pendingIntent = PendingIntent.getActivity(it,0,intent,0)

                val bitmapLargeIcon = BitmapFactory.decodeResource(activity?.applicationContext?.resources,
                    R.drawable.home_purple
                )


            var found = "We found the bounding boxes. It seems the picture contains Dog!"

            outputs?.let {
                    o->
                if(o[0].boxes?.isEmpty() == true){
                    found = "We couldn't the bounding boxes. It seems the picture doesn't contain Dog!"
                }
            }
                val builder = NotificationCompat.Builder(it, CHANNEL_ID)
                    .setSmallIcon(R.drawable.ic_launcher_foreground)
                    .setContentTitle("Finder Update!")
                    .setContentText(found)
                    .setLargeIcon(bitmapLargeIcon)
                    .setStyle(NotificationCompat.BigPictureStyle().bigPicture(img_url))
                    .setContentIntent(pendingIntent)
                    .setPriority(NotificationCompat.PRIORITY_HIGH)

                with(NotificationManagerCompat.from(it)){
                    notify(notificationId, builder.build())
                }
        }
    }

}