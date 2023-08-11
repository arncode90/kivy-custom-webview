package org.arncode;


import android.webkit.WebResourceRequest;
import android.webkit.WebResourceError;
import android.graphics.Bitmap;
import android.webkit.WebView;
import java.lang.String;


public interface CallbackWrapper {

    public void onPageStarted(WebView view, String url, Bitmap favicon);

    public void onPageFinished(WebView view, String url);

    public void onPageCommitVisible(WebView view, String url);

    public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error);

    public boolean shouldOverrideUrlLoading(String url);

}