#!/bin/bash
echo "Script Menu:"
echo "1: Prints Date
2: Prints the number of processes which are running currently
3: Prints the kernel name
4: Prints the kernel version
5: Prints the Kernel release
6: Prints the kernel dump or messages
7: Prints the RAM status
8: Prints the overall CPU usage
9: Prints the current user
10:Prints the Device IP
11:Prints the System uptime"

output_dir="$HOME/Downloads/output"

mkdir -p "$output_dir"

run_commands_automatically(){

        date > "$output_dir/today_date.txt"
        ps -aux > "$output_dir/running_processes.txt"
        uname --kernel-name > "$output_dir/kernel_name.txt"
        uname --kernel-version > "$output_dir/kernel_version.txt"
        uname --kernel-release > "$output_dir/kernel_release.txt"
        dmesg > "$output_dir/kernel_logs.txt"
        free -h > "$output_dir/ram_status.txt"
        top -bn1 | grep "Cpu(s)" | awk '{usage = 100 - $8; printf "Total CPU Usage: %.2f%%\n", usage}' > "$output_dir/cpu_usage.txt"
        whoami > "$output_dir/current_user.txt"
        ip addr show > "$output_dir/device_ip.txt"
        uptime > "$output_dir/uptime.txt"
}

run_commands_using_user_inputs(){
        read -p "Enter your choice:" input

        case $input in
                1)
                        echo "Saving today's date in today_date.txt"
                        date > "$output_dir/today_date.txt"
                        ;;

                2)
                        echo "Saving the current processes list in running_processes.txt"
                        ps -aux > "$output_dir/running_processes.txt"
                        ;;

                3)
                        echo "Saving the kernel name in kernel_name.txt"
                        uname --kernel-name > "$output_dir/kernel_name.txt"
                        ;;

                4)
                        echo "Saving Kernel version information in kernel_version.txt"
                        uname --kernel-version > "$output_dir/kernel_version.txt"
                        ;;
                5)
                        echo "Saving Kernel release information in kernel_release.txt"
                        uname --kernel-release > "$output_dir/kernel_release.txt"
                        ;;

                6)
                        echo "Saving Kernel logs in kernel_logs.txt"
                        dmesg >  "$output_dir/kernel_logs.txt"
                        ;;

                7)
                        echo "Saving RAM status in ram_status.txt"
                        free-h > "$output_dir/ram_status.txt"
                        ;;

                8)
                        echo "Saving CPU Usage in cpu_usage.txt"
                        top -bn1 | grep "Cpu(s)" | awk '{usage = 100 - $8; printf "Total CPU Usage: %.2f%%\n", usage}' > "$output_dir/cpu_usage.txt"
                        ;;

                9)
                        echo "Saving the current user in current_user.txt"
                        whoami > "$output_dir/current_user.txt"
                        ;;

                10)
                        echo "Saving Device ip in device_ip.txt"
                        ip addr show > "$output_dir/device_ip.txt"
                        ;;

                11)
                        echo "Saving uptime in uptime.txt"
                        uptime > "$output_dir/uptime.txt"
                        ;;

                *)
                        echo "Invalid Choice"
                        ;;
        esac


}

run_commands_using_user_inputs
run_commands_automatically
