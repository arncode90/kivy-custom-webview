package org.arncode;


import java.lang.String;
import android.view.View;
import android.graphics.Bitmap;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import org.arncode.CallbackWrapper;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceError;


public class CustomWebViewClient extends WebViewClient {

    public CallbackWrapper callback_wrapper;

    public CustomWebViewClient(CallbackWrapper callback_wrapper) {
	this.callback_wrapper = callback_wrapper;
    }

    @Override
    public void onPageStarted(WebView view, String url, Bitmap favicon) {
	this.callback_wrapper.onPageStarted(view, url, favicon);
    }

    @Override
    public void onPageFinished(WebView view, String url) {
	this.callback_wrapper.onPageFinished(view, url);
    }

    @Override
    public void onPageCommitVisible(WebView view, String url) {
	this.callback_wrapper.onPageCommitVisible(view, url);
    }

    @Override
    public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error) {
	this.callback_wrapper.onReceivedError(view, request, error);
    }

    @Override
    public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
    String url = request.getUrl().toString();
	this.callback_wrapper.shouldOverrideUrlLoading(url);
	return false;
    }
}