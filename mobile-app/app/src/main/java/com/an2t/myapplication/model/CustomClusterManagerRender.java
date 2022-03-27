package com.an2t.myapplication.model;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.Drawable;
import android.view.ViewGroup;
import android.widget.ImageView;

import androidx.annotation.NonNull;

import com.an2t.myapplication.R;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.maps.android.clustering.Cluster;
import com.google.maps.android.clustering.ClusterManager;
import com.google.maps.android.clustering.view.DefaultClusterRenderer;
import com.google.maps.android.ui.IconGenerator;
import com.squareup.picasso.Picasso;

public class CustomClusterManagerRender extends DefaultClusterRenderer<ClusterMarker> {

    private final IconGenerator iconGenerator;
    private ImageView imageView;

    public CustomClusterManagerRender(Context context, GoogleMap googleMap,
                                      ClusterManager<ClusterMarker> clusterManager) {

        super(context, googleMap, clusterManager);
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
                .into(imageView);

        Bitmap icon = iconGenerator.makeIcon();
        markerOptions.icon(BitmapDescriptorFactory.fromBitmap(icon)).title(item.getTitle());
        super.onBeforeClusterItemRendered(item, markerOptions);
    }

    @Override
    protected boolean shouldRenderAsCluster(@NonNull Cluster<ClusterMarker> cluster) {
        return false;
    }

}
