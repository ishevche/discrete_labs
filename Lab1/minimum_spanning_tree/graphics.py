import firebase_admin
import matplotlib.pyplot as plt
from firebase_admin import credentials, firestore


def get_firebase():
    cred = credentials.Certificate('firebase_token.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db


def main():
    doc = get_firebase().collection('dm_lab').document('prima')
    prima_y = list(map(lambda x: x[1],
                       sorted(doc.get().to_dict().items(),
                              key=lambda x: int(x[0]))))
    prima_x = list(map(lambda x: float(x[0]),
                       sorted(doc.get().to_dict().items(),
                              key=lambda x: int(x[0]))))

    plt.plot(prima_x, prima_y)

    plt.legend(['Graphic'])
    plt.xlabel('Vertices amount')
    plt.ylabel('Time consumed')
    plt.suptitle(f'Prim algorithm')
    plt.show()


if __name__ == '__main__':
    main()
