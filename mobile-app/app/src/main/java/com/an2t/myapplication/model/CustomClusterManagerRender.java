package com.an2t.myapplication.model;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.Drawable;
import android.view.ViewGroup;
import android.widget.ImageView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.an2t.myapplication.R;
import com.bumptech.glide.Glide;
import com.bumptech.glide.load.engine.DiskCacheStrategy;
import com.bumptech.glide.request.target.SimpleTarget;
import com.bumptech.glide.request.transition.Transition;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.material.imageview.ShapeableImageView;
import com.google.maps.android.clustering.Cluster;
import com.google.maps.android.clustering.ClusterManager;
import com.google.maps.android.clustering.view.DefaultClusterRenderer;
import com.google.maps.android.ui.IconGenerator;
import com.squareup.picasso.MemoryPolicy;
import com.squareup.picasso.NetworkPolicy;
import com.squareup.picasso.Picasso;

public class CustomClusterManagerRender extends DefaultClusterRenderer<ClusterMarker> {

    private final IconGenerator iconGenerator;
    private ImageView imageView;
//    private Context mContext;

    public CustomClusterManagerRender(Context context, GoogleMap googleMap,
                                      ClusterManager<ClusterMarker> clusterManager) {

        super(context, googleMap, clusterManager);

//        this.mContext = context;
        iconGenerator = new IconGenerator(context.getApplicationContext());
        imageView = new ImageView(context.getApplicationContext());

        int markerWidth = (int) context.getResources().getDimension(R.dimen.marker_size);
        int markerHeight = (int) context.getResources().getDimension(R.dimen.marker_size);
        imageView.setLayoutParams(new ViewGroup.LayoutParams(markerWidth, markerHeight));
        imageView.setScaleType(ImageView.ScaleType.CENTER_CROP);
        imageView.requestLayout();
        iconGenerator.setContentView(imageView);
    }

    @Override
    protected void onBeforeClusterItemRendered(@NonNull ClusterMarker item, @NonNull MarkerOptions markerOptions) {

        Picasso.get()
                .load(item.getUser().getImageUrl())
                .placeholder(R.drawable.gallery)
                .error(R.drawable.gallery)
                .into(new com.squareup.picasso.Target() {
                    @Override
                    public void onBitmapLoaded(Bitmap bitmap, Picasso.LoadedFrom from) {
                        imageView.setImageBitmap(bitmap);
                    }

                    @Override
                    public void onBitmapFailed(Exception e, Drawable errorDrawable) {

                    }

                    @Override
                    public void onPrepareLoad(Drawable placeHolderDrawable) {
                    }
                })
        ;

//        Picasso.get()
//                .load(item.getUser().getImageUrl())
//                .placeholder(R.drawable.gallery)
//                .error(R.drawable.gallery)
//                .into(imageView);

        Bitmap icon = iconGenerator.makeIcon();
        markerOptions.icon(BitmapDescriptorFactory.fromBitmap(icon)).title(item.getTitle());
        super.onBeforeClusterItemRendered(item, markerOptions);
    }

    @Override
    protected boolean shouldRenderAsCluster(@NonNull Cluster<ClusterMarker> cluster) {
        return false;
    }

}
