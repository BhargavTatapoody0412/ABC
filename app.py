import json
from sympy import symbols, expand
from sympy import N

# MileStone 1: To be able to read the json data.
def read_json(path):
    try:
        with open(path, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"The file {path} was not found")
    except json.JSONDecodeError:
        print(f"Cannot decode the json file: {path}")
    except Exception as e:
        print(f"Caught an exception: {e}")
    return None


# MileStone 2: To be able to decrypt the y value and get the points upto the k value.
def decrypt_value(base, value):
    return int(value, int(base))

# Milestone 3: Construct a polynomial using lagranges proportion
def construct_polynomial(points):
    x = symbols("x")
    k = len(points)

    def basis_polynomial(i):
        basis = 1
        xi, _ = points[i]

        for j in range(0,k):
            if j != i:
                xj, _ = points[j]
                basis *= (x - xj) / (xi - xj)
        
        return expand(basis)
    
    polynomial = 0
    for i in range(k):
        _, yi = points[i]
        polynomial += yi * basis_polynomial(i)
    
    return N(polynomial, 10)


# MileStone 4: Finding any wrong points in the json
def find_wrong_points(points, polynomial):
    x = symbols('x')
    wrong_points = []

    for point in points:
        xi, yi = point
        calculated_yi = polynomial.subs(x, xi)

        if not N(calculated_yi, 10).equals(yi):
            wrong_points.append(point)
    
    return wrong_points


def main(path):
    ## 1
    data = read_json(path)

    ## 2
    if data:
        
        keys = data.pop('keys')
        n = keys['n']
        k = keys['k']

        selected_keys = list(data.keys())[:k]
        points = []

        for key in selected_keys:
            x = int(key)
            
            base = data[key]['base']
            encrypted_val = data[key]['value']

            y = decrypt_value(base, encrypted_val)

            points.append((x,y))

        ## 3
        polynomial = construct_polynomial(points)
        print("Polynomial: ", polynomial)

        ## 4
        wrong_points = find_wrong_points(points, polynomial)
        print("Wrong points: ", wrong_points)



file_path = "./input.json"
main(file_path)