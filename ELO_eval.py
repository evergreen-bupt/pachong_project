import re
elo_dic={}
toy_data={"Update-vjw_10h_vs_Update-v6-17h":"3 / 15 (18)"}
K=32
def expected_result(player1_elo, player2_elo):
    return 1 / (1 + 10**((player2_elo - player1_elo) / 400))


for key,value in toy_data.items():
    model=key.split("_vs_")
    model_a=model[0]
    model_b=model[1]
    if model_a not in elo_dic:
        elo_dic[model_a]=1000
    if model_b not in elo_dic:
        elo_dic[model_b]=1000 
    numbers=re.findall(r'\d+',value)
    numbers=[int(number) for number in numbers]
    W_a = numbers[0] / numbers[2]
    W_b = numbers[1] / numbers[2]
    # print(model_a,model_b,numbers)
    E_a=expected_result(elo_dic[model_a],elo_dic[model_b])
    E_b=expected_result(elo_dic[model_b],elo_dic[model_a])
    elo_dic[model_a] = elo_dic[model_a] + K * (W_a - E_a)
    elo_dic[model_b] = elo_dic[model_b] + K * (W_b - E_b)
print(W_a,W_b,elo_dic)



