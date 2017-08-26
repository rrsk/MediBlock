package app.mediblocks.com.mediblocks;

import android.renderscript.Int2;

import static android.os.Build.VERSION_CODES.M;

/**
 * Created by RISHAB on 25-08-2017.
 */

class Pill {

    public String pillName;

    public String dosage = "";

    public Integer count ;

    public Pill(String name, String dose , Integer count){
        this.pillName = name;
        setDosage(dose);
        this.count = count;
    }

    public Pill() {
        this.pillName="";
        this.dosage="";
    }

    public void setDosage(String dose){
        dosage = "";
        for(int i=0; i<3; i++){
            if(i ==0 && dose.charAt(i)=='1'){
                dosage += " M ";
            }
            else if(i ==1 && dose.charAt(i)=='1'){
                dosage += " E ";
            }
            else if(i ==2 && dose.charAt(i)=='1'){
                dosage += " N ";
            }
        }
    }


    public void setName(String name){
        pillName = name;
    }

    public String getName(){
        return pillName;
    }

    public String getDosage(){
        return dosage;
    }
    public Integer getCount(){
        return this.count;
    }
}
