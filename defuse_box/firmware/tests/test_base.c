#define DEFUSE_HOST_TEST
#include "../User/main.c"
#include <assert.h>
#include <stdlib.h>
static unsigned hw_on,hw_pulse,beeps;
static char output[16000];
void console_write(const char *s){assert(strlen(output)+strlen(s)<sizeof(output));strcat(output,s);}
unsigned console_dropped(void){return 0u;}
void servo_set(unsigned on,unsigned p){hw_on=on;hw_pulse=p;}
void beep(uint32_t now){(void)now;beeps++;}
void led2_set(unsigned on){(void)on;}
int imu_init(Imu *s){memset(s,0,sizeof(*s));return 0;}
static void send(const char *s,uint32_t now){while(*s){rx_byte((uint8_t)*s++,now);}}
static void reset(void){used=discard=0u;servo_on=0u;pulse=1500u;hw_on=0u;page=0u;output[0]=0;}
int main(void)
{
    unsigned i;FILE *f;char path[128];
    reset();send("SERVO US 1500\r\n",0);assert(!hw_on&&strstr(output,"FIRST"));
    send("servo on\r\n",100);assert(hw_on&&pulse==1500u&&page==3u);
    send("SERVO US 1399\n",101);assert(pulse==1500u&&strstr(output,"ERR RANGE"));
    send("SERVO US 1601\n",101);assert(pulse==1500u);
    send("SERVO US 1500X\n",101);assert(pulse==1500u&&strstr(output,"FORMAT"));
    send("SERVO US +150\n",101);assert(pulse==1500u);
    send("SERVO US 1600\n",102);assert(pulse==1600u&&hw_pulse==1600u);
    rotate(500,103);assert(pulse==1600u);rotate(-500,104);assert(pulse==1400u);
    servo_task(15103);assert(hw_on);servo_task(15104);assert(!hw_on);
    start_servo(0xfffffff0u);servo_task(0xfffffff0u+14999u);assert(hw_on);
    servo_task(0xfffffff0u+15000u);assert(!hw_on);
    start_servo(0);send("PAGE 2\n",1);assert(!hw_on&&page==1u);
    start_servo(0);page=3u;handle_keys(3u,2);assert(!hw_on); /* Stop wins simultaneous start. */
    page=0u;handle_keys(1u,3);assert(!hw_on&&last_key==1u);
    page=3u;handle_keys(1u,4);assert(hw_on);handle_keys(8u,5);assert(!hw_on&&page==4u);
    handle_keys(8u,6);assert(page==0u);
    send("PAGE 5\n",7);assert(page==4u&&!hw_on);
    send("PAGE 6\n",8);assert(page==4u&&strstr(output,"UNKNOWN"));
    ui_init();display_init();draw(8u);
    f=fopen("Previews/page5.bin","wb");assert(f);assert(fwrite(display_framebuffer(),1,1024,f)==1024);fclose(f);
    for(i=0;i<1024u;i++){if(display_framebuffer()[i])break;}assert(i<1024u);
    handle_keys(7u,9);assert(page==4u&&!hw_on);
    reset();send("SER",1);assert(!hw_on);send("VO ON\r",2);assert(hw_on);stop_servo();
    for(i=0;i<90u;i++){rx_byte('A',3);}send("SERVO ON\n",3);assert(!hw_on&&strstr(output,"TOO LONG"));
    send("SERVO ON\n",4);assert(hw_on);stop_servo();
    rx_byte(0xffu,5);send("SERVO ON\n",5);assert(!hw_on);send("BEEP\r\n",6);assert(beeps==1u);
    reset();imu.online=1u;imu.last_good=100u;samples=0u;assert(!fresh(100u));
    samples=1u;assert(fresh(399u));assert(!fresh(400u));
    imu.id=0x70u;imu.a[0]=-32768;imu.a[1]=-32768;imu.a[2]=32767;
    samples=99999u;imu.errors=99999u;raw=filtered=4095u;light_ok=1u;light_at=100u;encoder_count=-9999;last_key=4;
    for(i=0;i<4;i++){
        display_init();page=i;draw(100u);assert(display_clipped_text()==0u);
        sprintf(path,"Previews/page%u.bin",i+1u);f=fopen(path,"wb");assert(f);assert(fwrite(display_framebuffer(),1,1024,f)==1024);fclose(f);
    }
    puts("PASS: pulse bounds; start/stop priority; inactivity and tick wrap; page stop; fragmented/overlong/non-ASCII commands; stale IMU; actual OLED text bounds.");
    return 0;
}
