package main

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

const (
	MaxX = 1100
	MaxY = 1100
)

type Point struct {
	x, y int
}

type Rectangle struct {
	id string
	topLeft, bottomRight Point
}

func makeInt(s []string) []int {
	result := make([]int, 0)
	for _, v := range s {
		i, _ := strconv.Atoi(v)
		result = append(result, i)
	}
	return result
}

func inner(p Point, r *Rectangle) bool {
	return p.x >= r.topLeft.x && p.x <= r.bottomRight.x &&
		   p.y >= r.topLeft.y && p.y <= r.bottomRight.y
}

func intersect(r1, r2 *Rectangle) bool {
	if r1.bottomRight.x < r2.topLeft.x || r2.bottomRight.x < r1.topLeft.x {
		return false
	}

	if r1.bottomRight.y < r2.topLeft.y || r2.bottomRight.y < r1.topLeft.y {
		return false
	}

	return true
}

func main() {
	input, _ := os.Open("input.txt")
	rectangles := make([]Rectangle, 0)

	for {
		var id, tmp2, c, size string
		_, err := fmt.Fscanf(input, "%s %s %s %s\n", &id, &tmp2, &c, &size)
		if err == io.EOF {
			break
		}
		top := makeInt(strings.Split(c[:len(c)-1], ","))
		sizes := makeInt(strings.Split(size, "x"))
		rectangles = append(rectangles, Rectangle{
			id: id[1:],
			topLeft:     Point{top[0], top[1]},
			bottomRight: Point{top[0] + sizes[0] - 1, top[1] + sizes[1] - 1},
		})
	}

	total := 0
	for i := 0; i < MaxX; i++ {
		for j := 0; j < MaxY; j++ {
			cnt := 0
			for k := 0; k < len(rectangles); k++ {
				if inner(Point{i, j}, &rectangles[k]) {
					cnt++
					if cnt > 1 {
						break
					}
				}
			}
			if cnt > 1 {
				total++
			}
		}
	}
	fmt.Println(total)

	c := make([]bool, len(rectangles))
	for i := 0; i < len(rectangles); i++ {
		for j := i+1; j < len(rectangles); j++ {
			if intersect(&rectangles[i], &rectangles[j]) {
				c[i] = true
				c[j] = true
			}
		}
	}
	for i := 0; i < len(rectangles); i++ {
		if !c[i] {
			fmt.Println(rectangles[i].id)
		}
	}
}
