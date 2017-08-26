package app.mediblocks.com.mediblocks;

/**
 * Created by luv on 15/4/17.
 */


import android.app.DownloadManager;
import android.content.Context;
import android.util.Log;
import android.widget.Toast;

import java.io.IOException;
import android.content.Context;
import android.util.Log;
import android.widget.Toast;

import java.io.IOException;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

import static android.content.ContentValues.TAG;


public class NetworkUtilities {
    //hrllo
    public static final MediaType JSON
            = MediaType.parse("application/json; charset=utf-8");

    public static final String BASE_URL_STRING = "";

    public static Response getRequest(Context ctx, String url_string){
        OkHttpClient client = new OkHttpClient();
        Request request = new Request.Builder()
//                    .addHeader()
                .url(url_string)
                .build();
        try{
            Log.i("TRYYY", "getRequest: 1");
            Response response = client.newCall(request).execute();
            if(response == null){
                Log.i("TRYYY", "getRequest: 1 NULL");
                Toast.makeText(ctx, "PLEASE CONNECT TO INTERNET", Toast.LENGTH_LONG).show();
            }
            else
            {
                Log.i("TRYYY", "getRequest: 1DONE hai ji");
            }
            return response;
        }catch (IOException ex){
            Log.i("TRYYY", "getRequest: 1");
            Toast.makeText(ctx, "error error error", Toast.LENGTH_SHORT).show();
            ex.printStackTrace();
            return null;
        }
    }


    public static Response postRequest(Context ctx, String json_string, String url_string){
        // TODO take care of ports in the constructor pf url
        OkHttpClient client = new OkHttpClient();
        try {
            RequestBody body = RequestBody.create(JSON, json_string);
            Request request = new Request.Builder()
                    .url(url_string)
                    .post(body)
                    .build();
            Response response = client.newCall(request).execute();
            return response;

//            if(response == null){
//                //Toast.makeText(ctx, "PLEASE CONNECT TO INTERNET", Toast.LENGTH_LONG).show();
////                Log.i("res", "postRequest: error");
//            }
//            return response;
        }catch (Exception e){
            e.printStackTrace();
            return null;
        }
    }




}


