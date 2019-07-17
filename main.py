from start_menu import run_menu

run_menu()

# ret_menu = 0
#
# actual_state = state_MENU
#
# while not stop:
#     if actual_state == state_MENU:
#         ret_menu = run_menu()
#         if ret_menu == 0:
#             stop = True
#         else:
#             actual_state = ret_menu
#
#     else:
#         if actual_state == state_HUMAN:
#             run_play_human()
#         elif actual_state == state_AI:
#             run_play_ai()
#         elif actual_state == state_TRAIN:
#             run_train()
#         elif actual_state == state_DRAW:
#             run_draw_map()
#
#         actual_state = state_MENU
