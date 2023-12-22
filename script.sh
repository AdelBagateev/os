#!/bin/bash 
 
# Game Stats Tracker 
total_turns=0 
successful_guesses=0 
failed_guesses=0 
last_picks=() 
correct_guess_indicator=() 
 
while true; do 
    # Generate a random number in the range [0, 9] 
    magic_number=((RANDOM % 10)) 
 
    # Prompt user for input 
    read -p "Round((total_turns + 1)): Enter a digit from 0 to 9 (type 'q' to quit): " user_pick 
 
    # Check if the user wants to quit 
    if [ "$user_pick" == "q" ]; then 
        echo "Game over. Thanks for playing!" 
        break 
    fi 
 
    # Validate user input 
    if ! [[ "$user_pick" =  ^[0-9]]]; then 
        echo "Error! Please enter a valid single-digit number from 0 to 9." 
        continue 
    fi 
 
    # Increment total turns 
    ((total_turns++)) 
 
    # Check if the guess is correct 
    if [ "$user_pick" -eq "$magic_number" ]; then 
        ((successful_guesses++)) 
        echo -e "[32mCorrect! Magic number: $magic_number[0m" 
        correct_guess_indicator+=(1) 
    else 
        ((failed_guesses++)) 
        echo -e "[31mIncorrect. Magic number: $magic_number[0m" 
        correct_guess_indicator+=(0) 
    fi 
 
    # Update last picks array 
    last_picks+=("$magic_number") 
    if [ "#last_picks[@]" -gt 10 ]; then 
        unset 'last_picks[0]' 
        last_picks=("last_picks[@]") 
        unset 'correct_guess_indicator[0]' 
        correct_guess_indicator=("correct_guess_indicator[@]") 
    fi 
 
    # Display game stats 
    echo "Game Stats:" 
    echo "Successful guesses: ((successful_guesses * 100 / total_turns))
    echo "Failed guesses:((failed_guesses * 100 / total_turns))
    echo "Last 10 numbers: " 
 
    index=0 
    while [ "$index" -lt "#last_picks[@]" ]; do 
        pick="last_picks[index]" 
        indicator="correct_guess_indicator[index]" 
 
        if [ "$indicator" -eq 1 ]; then 
            echo -n -e "[32m$pick[0m "  # Green color for correct guess (1) 
        elif [ "$indicator" -eq 0 ]; then 
            echo -n -e "[31m$pick[0m "  # Red color for incorrect guess (0) 
        else 
            echo "$pick" 
        fi 
 
        ((index++)) 
    done 
    echo "" 
done