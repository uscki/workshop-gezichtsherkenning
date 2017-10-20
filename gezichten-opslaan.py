import cv2, sys, os

def find_faces(face_cascade, image_dir):
    i, faces = 0, []
    for collection_id in os.listdir(image_dir):
        try:
            for file_id in os.listdir(os.path.join(image_dir, '%s/normal/' % collection_id)):
                i += 1
                if (i % 100) == 0:
                    print('now at', i, file=sys.stderr)
                fpath = os.path.join(image_dir, '%s/normal/%s' % (collection_id, file_id))
                try:
                    img = cv2.imread(fpath)
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    for (x,y,w,h) in face_cascade.detectMultiScale(gray, 1.3, 5):
                        yield collection_id, file_id, x,y,w,h
                except Exception as e:
                    print('problem with', collection_id, file_id, file=sys.stderr)
                    print(e, file=sys.stderr)
        except Exception as e:
            print('problem with collection', collection_id, file=sys.stderr)
            

if __name__ == '__main__':
    import sys
    try:
        _, cascade_path, image_dir = sys.argv
    except Exception as e:
        print('Usage: python3 gezichten-opslaan.py <cascade_path> <image_dir>\n')
        raise e
    
    face_cascade = cv2.CascadeClassifier(cascade_path)
    
    for (collection_id, file_id, x,y,w,h) in find_faces(face_cascade, image_dir):
        print(
            collection_id,
            file_id,
            x,
            y,
            x+w,
            y+h,
        sep='\t')
        sys.stdout.flush()
