#! /bin/bash
FRAMES=120
THREADS=4
FPS=30
FILENAME=out.avi
rm -f ./water/*.out.ppm $FILENAME
for i in `seq 1 $THREADS 120`
do
    jmax=`expr $i + $THREADS - 1`
    for j in `seq $i $jmax`
    do
        echo $j / 120
        infile=`printf "./water/%04d.ppm" $j`
        outfile=`printf "./water/%04d.out.ppm" $j`
        thread=`expr $j % $THREADS`
        if [ $thread == 0 ]
        then # Block on every fourth thread so there aren't too many running
            ./process $infile $outfile>/dev/null
        else # Run the other rendering calls in parallel
            ./process $infile $outfile >/dev/null &
        fi
    done
done
ffmpeg -y -stream_loop 20 -r $FPS -i ./water/%04d.out.ppm -c:v libx264 -vf fps=$FPS -pix_fmt yuv420p $FILENAME
rm -f ./water/*.out.ppm 
echo Done
echo "\a"
