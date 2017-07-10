#!/bin/sh
#
#	Action	Time `date -R`		Author		Version	Discription
#	Create	"Mon, 21 Nov 2016"	"Jason Fu"	v0.1	"Generate images for QFIL Download release."
#

if [ -z $LUNCH_TARGET ];then
	LUNCH_TARGET=aione
fi
sign_and_update_help()
{
  echo \
    "Usage:
  $0 all|xbl|prog|pmic|tz|hyp|keymaster|cmnlib|cmnlib64|devcfg|qsee|rpm|lk|adsp|tzapps|modem|mba|slpi|venus|mcfg|nonhlos|a530_zap|clean
  Example:
  $0 xbl
  $0 all
  $0 clean
  $0 single xbl xbl.elf"
  exit 1
}

sign_image()
{
  src_dir=$1
  sign_id=$2
  sign_name=$3
  if_copy_to_out=$4
  if_copy_to_src=$5

  echo "-------------------- signing $sign_name --------------------" | tee -a $signing_log
  #echo "src_dir=$src_dir" | tee -a $signing_log
  #echo "sign_id=$sign_id" | tee -a $signing_log
  #echo "sign_name=$sign_name" | tee -a $signing_log
  #echo "if_copy_to_out=$if_copy_to_out" | tee -a $signing_log
  if [ ! -f $src_dir/$sign_name ]; then
          echo "###ERROR source file: $src_dir/$sign_name is not found!" | tee -a $signing_log
          exit;
  fi
  cp $src_dir/$sign_name $RELEASE_DIR/unsigned/
  python $SECTOOL_DIR/sectools.py secimage -i $RELEASE_DIR/unsigned/$sign_name -c $CMIT_AIONE_SECIMAGE_XML -o $RELEASE_DIR/signed -sa >> $signing_log
  if [ -f $RELEASE_DIR/signed/8996/$sign_id/$sign_name ]; then
    echo "Signed file: $RELEASE_DIR/signed/8996/$sign_id/$sign_name" | tee -a $signing_log
    if [ -n "$if_copy_to_out" ]; then
      if [ "X${sign_id}" != "Xpmic" ];then
        cp $RELEASE_DIR/signed/8996/$sign_id/$sign_name $RELEASE_DIR/out
      else
        cp $RELEASE_DIR/signed/8996/$sign_id/$sign_name $RELEASE_DIR/out/$(echo $sign_name | tr A-Z a-z)
      fi
      echo "cp $RELEASE_DIR/signed/8996/$sign_id/$sign_name $RELEASE_DIR/out" | tee -a $signing_log
    fi
    if [ -n "$if_copy_to_src" ]; then
      if [ "X${sign_id}" != "Xpmic" ];then
        cp $RELEASE_DIR/signed/8996/$sign_id/$sign_name $(echo $src_dir | sed 's#\/unsigned##g')/$sign_name
      else
        cp $RELEASE_DIR/signed/8996/$sign_id/$sign_name $(echo $src_dir | sed 's#\/unsigned##g')/$(echo $sign_name | tr A-Z a-z)
      fi
      echo "cp $RELEASE_DIR/signed/8996/$sign_id/$sign_name $(echo $src_dir | sed 's#\/unsigned##g')/$sign_name" | tee -a $signing_log
    fi
  else
    echo "###ERROR target file: $RELEASE_DIR/signed/8996/$sign_id/$sign_name is not found!" | tee -a $signing_log
    exit;
  fi
}

signing_adsp()
{
  #ADSP
  sign_image $META_BUILD_DIR/adsp_proc/obj/qdsp6v5_ReleaseG adsp adsp.mbn
  cp $RELEASE_DIR/signed/8996/adsp/adsp.mbn $META_BUILD_DIR/adsp_proc/obj/qdsp6v5_ReleaseG/adsp.mbn
  echo "cp $RELEASE_DIR/signed/8996/adsp/adsp.mbn $META_BUILD_DIR/adsp_proc/obj/qdsp6v5_ReleaseG/adsp.mbn" | tee -a $signing_log
}

signing_tzapps()
{
  #TZApps
  ta_name_list="cppf.mbn fingerprint64.mbn goodixfp.mbn gptest.mbn iris.mbn isdbtmm.mbn mdtp.mbn qmpsecap.mbn securemm.mbn smplap32.mbn smplap64.mbn widevine.mbn cmnlib.mbn cmnlib64.mbn"
  ta_sign_id_list="cppf fingerprint64 goodixfp gptest iris isdbtmm mdtp qmpsecap securemm sampleapp32 sampleapp64 widevine cmnlib cmnlib64"

  for ta_name in $ta_name_list
  do
    tmp=`echo $ta_sign_id_list | sed 's/^[a-zA-Z0-9]* //'`
    ta_sign_id=`echo $ta_sign_id_list | sed 's/ .*$//'`
    ta_sign_id_list=$tmp
    #echo "ta_name=$ta_name, ta_sign_id=$ta_sign_id." | tee -a $signing_log
    sign_image $META_BUILD_DIR/trustzone_images/build/ms/bin/IADAANAA $ta_sign_id $ta_name
    cp $RELEASE_DIR/signed/8996/$ta_sign_id/$ta_name $META_BUILD_DIR/trustzone_images/build/ms/bin/IADAANAA/$ta_name
    echo "cp $RELEASE_DIR/signed/8996/$ta_sign_id/$ta_name $META_BUILD_DIR/trustzone_images/build/ms/bin/IADAANAA/$ta_name" | tee -a $signing_log
  done
}

signing_modem()
{
  echo "-------------------- signing $sign_name --------------------" | tee -a $signing_log
  if [ ! -f $META_BUILD_DIR/modem_proc/build/ms/bin/8996.gen.prod/qdsp6sw.mbn ]; then
          echo "###ERROR $META_BUILD_DIR/modem_proc/build/ms/bin/8996.gen.prod/qdsp6sw.mbn is not found!" | tee -a $signing_log
          exit;
  fi
  cp $META_BUILD_DIR/modem_proc/build/ms/bin/8996.gen.prod/qdsp6sw.mbn $RELEASE_DIR/unsigned/
  python $SECTOOL_DIR/sectools.py secimage -i $RELEASE_DIR/unsigned/qdsp6sw.mbn -c $CMIT_AIONE_SECIMAGE_XML -o $RELEASE_DIR/signed -sa >> $signing_log
  if [ -f $RELEASE_DIR/signed/8996/modem/modem.mbn ]; then
    echo "Signed file: $RELEASE_DIR/signed/8996/modem/modem.mbn" | tee -a $signing_log
  else
    echo "###ERROR $RELEASE_DIR/signed/8996/$sign_id/$sign_name is not found!" | tee -a $signing_log
    exit;
  fi

  cp $RELEASE_DIR/signed/8996/modem/modem.mbn $META_BUILD_DIR/modem_proc/build/ms/bin/8996.gen.prod/qdsp6sw.mbn
  echo "cp $RELEASE_DIR/signed/8996/modem/modem.mbn $META_BUILD_DIR/modem_proc/build/ms/bin/8996.gen.prod/qdsp6sw.mbn" | tee -a $signing_log
}

signing_mba()
{
  sign_image $META_BUILD_DIR/modem_proc/build/ms/bin/8996.gen.prod mba mba.mbn
  cp $RELEASE_DIR/signed/8996/mba/mba.mbn $META_BUILD_DIR/modem_proc/build/ms/bin/8996.gen.prod/mba.mbn
  echo "cp $RELEASE_DIR/signed/8996/mba/mba.mbn $META_BUILD_DIR/modem_proc/build/ms/bin/8996.gen.prod/mba.mbn" | tee -a $signing_log
}

signing_slpi()
{
  sign_image $META_BUILD_DIR/slpi_proc/obj/qdsp6v5_ReleaseG slpi slpi.mbn
  cp $RELEASE_DIR/signed/8996/slpi/slpi.mbn $META_BUILD_DIR/slpi_proc/obj/qdsp6v5_ReleaseG/slpi.mbn
  echo "cp $RELEASE_DIR/signed/8996/slpi/slpi.mbn $META_BUILD_DIR/slpi_proc/obj/qdsp6v5_ReleaseG/slpi.mbn" | tee -a $signing_log
}

signing_venus()
{
  sign_image $META_BUILD_DIR/venus_proc/build/bsp/asic/build/PROD/mbn/reloc/signed venus venus.mbn
  cp $RELEASE_DIR/signed/8996/venus/venus.mbn $META_BUILD_DIR/venus_proc/build/bsp/asic/build/PROD/mbn/reloc/signed/venus.mbn
  echo "cp $RELEASE_DIR/signed/8996/venus/venus.mbn $META_BUILD_DIR/venus_proc/build/bsp/asic/build/PROD/mbn/reloc/signed/venus.mbn" | tee -a $signing_log
}

signing_mcfg()
{
  echo "-------------------- signing mcfg files --------------------" | tee -a $signing_log
  mcfg_sw_file_list=`find $META_BUILD_DIR/modem_proc/mcfg/configs/ -name "mcfg_sw.mbn" -type f`
  mcfg_hw_file_list=`find $META_BUILD_DIR/modem_proc/mcfg/configs/ -name "mcfg_hw.mbn" -type f`

  for file in $mcfg_sw_file_list
  do
    #echo "mcfg_sw_file=$file"
    if [ ! -f $file ]; then
      echo "###ERROR $file is not found!" | tee -a $signing_log
      exit;
    fi
    cp $file $RELEASE_DIR/unsigned/
    python $SECTOOL_DIR/sectools.py secimage -i $RELEASE_DIR/unsigned/mcfg_sw.mbn -c $CMIT_AIONE_SECIMAGE_XML -o $RELEASE_DIR/signed -sa >> $signing_log
    if [ -f $RELEASE_DIR/signed/8996/mcfg_sw/mcfg_sw.mbn ]; then
      cp $RELEASE_DIR/signed/8996/mcfg_sw/mcfg_sw.mbn $file
      echo "cp $RELEASE_DIR/signed/8996/mcfg_sw/mcfg_sw.mbn $file" | tee -a $signing_log
    else
      echo "###ERROR $RELEASE_DIR/signed/8996/mcfg_sw/mcfg_sw.mbn is not found!" | tee -a $signing_log
      exit;
    fi
  done

  for file in $mcfg_hw_file_list
  do
    #echo "mcfg_hw_file=$file"
    if [ ! -f $file ]; then
      echo "###ERROR $file is not found!" | tee -a $signing_log
      exit;
    fi
    cp $file $RELEASE_DIR/unsigned/
    python $SECTOOL_DIR/sectools.py secimage -i $RELEASE_DIR/unsigned/mcfg_hw.mbn -c $CMIT_AIONE_SECIMAGE_XML -o $RELEASE_DIR/signed -sa >> $signing_log
    if [ -f $RELEASE_DIR/signed/8996/mcfg_hw/mcfg_hw.mbn ]; then
      cp $RELEASE_DIR/signed/8996/mcfg_hw/mcfg_hw.mbn $file
      echo "cp $RELEASE_DIR/signed/8996/mcfg_hw/mcfg_hw.mbn $file" | tee -a $signing_log
    else
      echo "###ERROR $RELEASE_DIR/signed/8996/mcfg_hw/mcfg_hw.mbn is not found!" | tee -a $signing_log
      exit;
    fi
  done
}

signing_a530_zap()
{
  if [ $OUT_PATH ];then
    sign_image $OUT_PATH/system/etc/firmware gfx_microcode a530_zap.elf
    cp $RELEASE_DIR/signed/8996/gfx_microcode/a530_zap.* $OUT_PATH/system/etc/firmware/
    echo "cp $RELEASE_DIR/signed/8996/gfx_microcode/a530_zap.* $OUT_PATH/system/etc/firmware/" | tee -a $signing_log
  else
    sign_image $CAF_BUILD_DIR/vendor/qcom/proprietary/prebuilt_HY11/target/product/msm8996/system/etc/firmware gfx_microcode a530_zap.elf
    cp $RELEASE_DIR/signed/8996/gfx_microcode/a530_zap.* $CAF_BUILD_DIR/vendor/qcom/proprietary/prebuilt_HY11/target/product/msm8996/system/etc/firmware/
    echo "cp $RELEASE_DIR/signed/8996/gfx_microcode/a530_zap.* $CAF_BUILD_DIR/vendor/qcom/proprietary/prebuilt_HY11/target/product/msm8996/system/etc/firmware/" | tee -a $signing_log
  fi
}

update_nonhlos()
{
  echo "-------------------- update NON-HLOS.bin --------------------" | tee -a $signing_log
  signing_adsp
  signing_tzapps
  signing_modem
  signing_mba
  signing_slpi
  signing_venus
  signing_mcfg
  cd $META_BUILD_DIR/common/build
  echo "python build.py --nonhlos >> $signing_log" | tee -a $signing_log
  python build.py --nonhlos >> $signing_log
  cp $META_BUILD_DIR/common/build/ufs/bin/asic/NON-HLOS.bin $RELEASE_DIR/out
  echo "cp $META_BUILD_DIR/common/build/ufs/bin/asic/NON-HLOS.bin $RELEASE_DIR/out" | tee -a $signing_log
}

clean()
{
  rm -f $signing_log
  rm -rf $RELEASE_DIR/unsigned
  rm -rf $RELEASE_DIR/signed
  rm -rf $RELEASE_DIR/out
}

sign_single_image()
{
  export RELEASE_DIR=$PWD
  export META_BUILD_DIR=`cd ../../../ && pwd`
  export SECTOOL_DIR=$META_BUILD_DIR/common/sectools
  export CMIT_AIONE_SECIMAGE_XML=$RELEASE_DIR/cmti_aione_secimage.xml

  export signing_log=$RELEASE_DIR/signing_log

  supported_sign_id_list="xbl prog_ufs_ddr pmic tz hyp keymaster cmnlib cmnlib64 devcfg rpm appsbl adsp cppf fingerprint64 goodixfp gptest iris isdbtmm mdtp qmpsecap securemm sampleapp32 sampleapp64 widevine modem mba slpi venus mcfg_sw mcfg_hw gfx_microcode "

  for sign_id in $supported_sign_id_list
  do
    #echo "\$2=$2, \$3=$3, sign_id=$sign_id."
    if [ $2 = $sign_id ]; then
      if [ -f $3 ]; then
        mkdir -p $RELEASE_DIR/signed
        mkdir -p $RELEASE_DIR/out
        python $SECTOOL_DIR/sectools.py secimage -i $3 -c $CMIT_AIONE_SECIMAGE_XML -o $RELEASE_DIR/signed -sa  >> $signing_log
        echo "File $3 has been signed and signed file can be found in signed dir" | tee -a $signing_log
        exit;
      else
        echo "###ERROR file: Signing file $3 can not be found!" | tee -a $signing_log
        exit;
      fi
    else
      echo "###ERROR sign_id: $2 isn't supported!" | tee -a $signing_log
      exit;
    fi
  done
}

main()
{
  export RELEASE_DIR=$PWD
  #export META_BUILD_DIR=/media/banana/work_space/amss
  export META_BUILD_DIR=`cd ../../../ && pwd`
  #export CAF_BUILD_DIR=/media/banana/work_space/caf
  if [ $CAF_BUILDSPACE ];then
    export CAF_BUILD_DIR=$CAF_BUILDSPACE
  else
    export CAF_BUILD_DIR=$META_BUILD_DIR/LINUX/android
  fi
  export SECTOOL_DIR=$META_BUILD_DIR/common/sectools
  export CMIT_AIONE_SECIMAGE_XML=$RELEASE_DIR/cmti_aione_secimage.xml

  export signing_log=$RELEASE_DIR/signing_log

  echo RELEASE_DIR=$RELEASE_DIR
  echo META_BUILD_DIR=$META_BUILD_DIR
  echo SECTOOL_DIR=$SECTOOL_DIR

  echo "-------------------- sign and update `date` --------------------" | tee -a $signing_log
  mkdir -p $RELEASE_DIR/unsigned
  mkdir -p $RELEASE_DIR/signed
  mkdir -p $RELEASE_DIR/out

  echo "-------------------- cmdline input: $0 $@ --------------------" | tee -a $signing_log
  case $1 in
    xbl)
      sign_image $META_BUILD_DIR/boot_images/QcomPkg/Msm8996Pkg/Bin64/unsigned xbl xbl.elf true
      exit;;
    prog)
      sign_image $META_BUILD_DIR/boot_images/QcomPkg/Msm8996Pkg/Bin64/unsigned prog_ufs_ddr prog_ufs_firehose_8996_ddr.elf true
      exit;;
    pmic)
      sign_image $META_BUILD_DIR/boot_images/QcomPkg/Msm8996Pkg/Bin64/unsigned pmic Pmic.elf
      cp $RELEASE_DIR/signed/8996/pmic/Pmic.elf $RELEASE_DIR/out/pmic.elf
      echo "cp $RELEASE_DIR/signed/8996/pmic/Pmic.elf $RELEASE_DIR/out/pmic.elf"
      exit;;
    tz)
      sign_image $META_BUILD_DIR/trustzone_images/build/ms/bin/IADAANAA tz tz.mbn true
      exit;;
    hyp)
      sign_image $META_BUILD_DIR/trustzone_images/build/ms/bin/IADAANAA hyp hyp.mbn true
      exit;;
    keymaster)
      sign_image $META_BUILD_DIR/trustzone_images/build/ms/bin/IADAANAA keymaster keymaster.mbn true
      exit;;
    cmnlib)
      sign_image $META_BUILD_DIR/trustzone_images/build/ms/bin/IADAANAA cmnlib cmnlib.mbn true
      exit;;
    cmnlib64)
      sign_image $META_BUILD_DIR/trustzone_images/build/ms/bin/IADAANAA cmnlib64 cmnlib64.mbn true
      exit;;
    devcfg)
      sign_image $META_BUILD_DIR/trustzone_images/build/ms/bin/IADAANAA devcfg devcfg.mbn true
      exit;;
    qsee)
      sign_image $META_BUILD_DIR/trustzone_images/build/ms/bin/IADAANAA tz tz.mbn true
      sign_image $META_BUILD_DIR/trustzone_images/build/ms/bin/IADAANAA hyp hyp.mbn true
      sign_image $META_BUILD_DIR/trustzone_images/build/ms/bin/IADAANAA keymaster keymaster.mbn true
      sign_image $META_BUILD_DIR/trustzone_images/build/ms/bin/IADAANAA cmnlib cmnlib.mbn true
      sign_image $META_BUILD_DIR/trustzone_images/build/ms/bin/IADAANAA cmnlib64 cmnlib64.mbn true
      sign_image $META_BUILD_DIR/trustzone_images/build/ms/bin/IADAANAA devcfg devcfg.mbn true
      exit;;
    rpm)
      sign_image $META_BUILD_DIR/rpm_proc/build/ms/bin/AAAAANAAR rpm rpm.mbn true
      exit;;
    lk)
      if [ $OUT_PATH ];then
        sign_image $OUT_PATH appsbl emmc_appsboot.mbn true
      else
        sign_image $CAF_BUILD_DIR/out/target/product/$LUNCH_TARGET appsbl emmc_appsboot.mbn true
      fi
      exit;;
    adsp)
      signing_adsp
      exit;;
    tzapps)
      signing_tzapps
      exit;;
    modem)
      signing_modem
      exit;;
    mba)
      signing_mba
      exit;;
    slpi)
      signing_slpi
      exit;;
    venus)
      signing_venus
      exit;;
    mcfg)
      signing_mcfg
      exit;;
    nonhlos)
      update_nonhlos
      exit;;
    a530_zap)
      signing_a530_zap
      exit;;
    clean)
      clean
      exit;;
    all)
      sign_image $META_BUILD_DIR/boot_images/QcomPkg/Msm8996Pkg/Bin64/unsigned xbl xbl.elf true true
      sign_image $META_BUILD_DIR/boot_images/QcomPkg/Msm8996Pkg/Bin64/unsigned prog_ufs_ddr prog_ufs_firehose_8996_ddr.elf true true
      sign_image $META_BUILD_DIR/boot_images/QcomPkg/Msm8996Pkg/Bin64/unsigned pmic Pmic.elf true true
      sign_image $META_BUILD_DIR/trustzone_images/build/ms/bin/IADAANAA tz tz.mbn true true
      sign_image $META_BUILD_DIR/trustzone_images/build/ms/bin/IADAANAA hyp hyp.mbn true true
      sign_image $META_BUILD_DIR/trustzone_images/build/ms/bin/IADAANAA keymaster keymaster.mbn true true
      sign_image $META_BUILD_DIR/trustzone_images/build/ms/bin/IADAANAA cmnlib cmnlib.mbn true true
      sign_image $META_BUILD_DIR/trustzone_images/build/ms/bin/IADAANAA cmnlib64 cmnlib64.mbn true true
      sign_image $META_BUILD_DIR/trustzone_images/build/ms/bin/IADAANAA devcfg devcfg.mbn true true
      sign_image $META_BUILD_DIR/rpm_proc/build/ms/bin/AAAAANAAR rpm rpm.mbn true true
      if [ $OUT_PATH ];then
        sign_image $OUT_PATH appsbl emmc_appsboot.mbn true true
      else
        sign_image $CAF_BUILD_DIR/out/target/product/$LUNCH_TARGET appsbl emmc_appsboot.mbn true true
      fi
      signing_a530_zap
      update_nonhlos
      exit;;
    *)
      echo "##### OPTION:$1 is not supported #####"
      exit;;
  esac
}

case $1 in
  all|xbl|prog|pmic|tz|hyp|keymaster|cmnlib|cmnlib64|devcfg|qsee|rpm|lk|adsp|tzapps|modem|mba|slpi|venus|mcfg|nonhlos|a530_zap|clean)
    export PATH=./:$PATH
    main $@;;
  single)
    sign_single_image $@;;
  *)
    sign_and_update_help;;
esac
