program ozone_process

    implicit none
    integer:: year, mon, day
    integer:: i, j, a, b, c, la, lo, z
    integer::ozo(360,180) !オゾンデータ配列 
    real::oz(360,180)
    character::em,str_year*4,str_mon*2,str_day*2
  

    ! define year
  	! write(6,*) 'input year'
  	! read(5,*) year
    year=2020  

    ! define month
    ! write(6,*) 'input month '
    ! read(5,*) mon
    mon=9
    ! define day
    ! write(6,*) 'input day'
    ! read(5,*) day
    day=20
    ! transform int to str 
  	write(str_year,'(i4)') year
    write(str_mon,'(i2.2)') mon
    write(str_day,'(i2.2)') day


    ! ファイルの読み込み
    ! open(10,file='https://ozonewatch.gsfc.nasa.gov/data/omi/Y'//str_year//'/&
    ! L3_ozone_omi_'//str_year//''//str_mon//''//str_day//'.txt',&
    ! form='formatted',status="old")
    open(10,file='L3_ozone_omi_20200920.txt',&
    form='formatted',status="old")

    ! 3行読み飛ばす
    do i=1,3
        read(10,*)
    end do
    ! 1つの格子点当たり（25個　×　14行　のデータ配列）＋（10個　×　1行　のデータ配列）
  
    do la=1,180
        a=1
        !read(10,'(A1)')
        do i=1,14
          b=a+24
          read(10,'(A1,25I3)') em,(ozo(lo,la),lo=a,b)
          a=a+25
        end do
        c=a+9
        read(10,'(A1,10I3)') em,(ozo(lo,la),lo=a,c)
    end do
  
    close(10)

    
    ! 新規ファイル作成
    open(11,file='ozonedata_'//str_year//''//str_mon//''//str_day//'.txt',&
            form="formatted")
    open(12,file='ex_ozonedata_'//str_year//''//str_mon//''//str_day//'.txt',&
            form="formatted")

    ! 新規ファイルに書き込み
            do la=1,180    
                ! do lo=1,360
                    write(11,'(360I3)') (ozo(lo,la),lo=1,360)
                    write(12,*) (ozo(lo,la),lo=1,360)
                ! enddo
            enddo

            


end program ozone_process
