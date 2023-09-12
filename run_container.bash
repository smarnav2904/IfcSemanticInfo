
xhost +local:docker
docker run -it \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix" \
    --net=host \
    --privileged \
    --mount type=bind,source=/home/santi/IfcSemanticInfo/exchange,target=/home/rva_container/rva_exchange \
    nordic \
    bash
    
    
